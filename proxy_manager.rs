use std::collections::HashMap;
use std::sync::{Arc, Mutex};
use std::time::{Duration, Instant};
use tokio::time::sleep;
use reqwest::{Client, Proxy};
use serde::{Deserialize, Serialize};
use rand::seq::SliceRandom;

#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct ProxyInfo {
    pub ip: String,
    pub port: u16,
    pub country: String,
    pub protocol: String,
    pub speed: f64,
    pub success_rate: f64,
    #[serde(skip, default = "Instant::now")]
    pub last_tested: Instant,
    pub failures: u32,
}

#[derive(Debug, Clone)]
pub struct ProxyManager {
    proxies: Arc<Mutex<Vec<ProxyInfo>>>,
    working_proxies: Arc<Mutex<HashMap<String, Vec<ProxyInfo>>>>,
    client: Client,
}

impl ProxyManager {
    pub fn new() -> Self {
        Self {
            proxies: Arc::new(Mutex::new(Vec::new())),
            working_proxies: Arc::new(Mutex::new(HashMap::new())),
            client: Client::new(),
        }
    }

    pub async fn fetch_free_proxies(&self) -> Result<(), Box<dyn std::error::Error>> {
        let sources = vec![
            "https://www.proxy-list.download/api/v1/get?type=http",
            "https://raw.githubusercontent.com/TheSpeedX/PROXY-List/master/http.txt",
            "https://raw.githubusercontent.com/clarketm/proxy-list/master/proxy-list-raw.txt",
            "https://raw.githubusercontent.com/ShiftyTR/Proxy-List/master/http.txt",
            "https://raw.githubusercontent.com/monosans/proxy-list/main/proxies/http.txt",
        ];

        let mut all_proxies = Vec::new();

        for source in sources {
            if let Ok(response) = self.client.get(source).send().await {
                if let Ok(text) = response.text().await {
                    let proxies = self.parse_proxy_list(&text);
                    all_proxies.extend(proxies);
                }
            }
        }

        // Add country-specific proxy sources
        self.fetch_country_proxies(&mut all_proxies).await;

        let mut proxy_list = self.proxies.lock().unwrap();
        proxy_list.extend(all_proxies);
        
        Ok(())
    }

    async fn fetch_country_proxies(&self, proxies: &mut Vec<ProxyInfo>) {
        let country_sources = vec![
            ("US", "https://raw.githubusercontent.com/proxy4parsing/proxy-list/main/http_us.txt"),
            ("UK", "https://raw.githubusercontent.com/proxy4parsing/proxy-list/main/http_uk.txt"),
            ("CA", "https://raw.githubusercontent.com/proxy4parsing/proxy-list/main/http_ca.txt"),
            ("DE", "https://raw.githubusercontent.com/proxy4parsing/proxy-list/main/http_de.txt"),
            ("FR", "https://raw.githubusercontent.com/proxy4parsing/proxy-list/main/http_fr.txt"),
        ];

        for (country, url) in country_sources {
            if let Ok(response) = self.client.get(url).send().await {
                if let Ok(text) = response.text().await {
                    let mut country_proxies = self.parse_proxy_list(&text);
                    for proxy in &mut country_proxies {
                        proxy.country = country.to_string();
                    }
                    proxies.extend(country_proxies);
                }
            }
        }
    }

    fn parse_proxy_list(&self, text: &str) -> Vec<ProxyInfo> {
        let mut proxies = Vec::new();
        
        for line in text.lines() {
            let line = line.trim();
            if line.is_empty() || line.starts_with('#') {
                continue;
            }

            if let Some((ip, port_str)) = line.split_once(':') {
                if let Ok(port) = port_str.parse::<u16>() {
                    proxies.push(ProxyInfo {
                        ip: ip.to_string(),
                        port,
                        country: "Unknown".to_string(),
                        protocol: "http".to_string(),
                        speed: 0.0,
                        success_rate: 0.0,
                        last_tested: Instant::now(),
                        failures: 0,
                    });
                }
            }
        }

        proxies
    }

    pub async fn test_proxies(&self) -> Result<(), Box<dyn std::error::Error>> {
        let proxies = {
            let proxy_list = self.proxies.lock().unwrap();
            proxy_list.clone()
        };

        let mut working = HashMap::new();
        let test_urls = vec![
            "http://httpbin.org/ip",
            "http://icanhazip.com",
            "http://ipinfo.io/ip",
        ];

        for proxy in proxies {
            let proxy_url = format!("http://{}:{}", proxy.ip, proxy.port);
            
            if let Ok(proxy_client) = reqwest::Client::builder()
                .proxy(Proxy::http(&proxy_url)?)
                .timeout(Duration::from_secs(10))
                .build()
            {
                let start = Instant::now();
                let mut success_count = 0;

                for test_url in &test_urls {
                    if let Ok(response) = proxy_client.get(*test_url).send().await {
                        if response.status().is_success() {
                            success_count += 1;
                        }
                    }
                }

                let speed = start.elapsed().as_millis() as f64;
                let success_rate = success_count as f64 / test_urls.len() as f64;

                if success_rate > 0.5 {
                    let mut updated_proxy = proxy.clone();
                    updated_proxy.speed = speed;
                    updated_proxy.success_rate = success_rate;
                    updated_proxy.last_tested = Instant::now();

                    working.entry(updated_proxy.country.clone())
                        .or_insert_with(Vec::new)
                        .push(updated_proxy);
                }
            }
        }

        let mut working_proxies = self.working_proxies.lock().unwrap();
        *working_proxies = working;

        Ok(())
    }

    pub fn get_proxy_by_country(&self, country: &str) -> Option<ProxyInfo> {
        let working_proxies = self.working_proxies.lock().unwrap();
        
        if let Some(country_proxies) = working_proxies.get(country) {
            if !country_proxies.is_empty() {
                let mut rng = rand::thread_rng();
                return country_proxies.choose(&mut rng).cloned();
            }
        }

        // Fallback to any working proxy
        for proxies in working_proxies.values() {
            if !proxies.is_empty() {
                let mut rng = rand::thread_rng();
                return proxies.choose(&mut rng).cloned();
            }
        }

        None
    }

    pub fn get_best_proxy(&self, country: Option<&str>) -> Option<ProxyInfo> {
        let working_proxies = self.working_proxies.lock().unwrap();
        
        let mut best_proxy: Option<ProxyInfo> = None;
        let mut best_score = 0.0;

        let proxies_to_check = if let Some(country) = country {
            if let Some(country_proxies) = working_proxies.get(country) {
                vec![country_proxies]
            } else {
                working_proxies.values().collect()
            }
        } else {
            working_proxies.values().collect()
        };

        for proxies in proxies_to_check {
            for proxy in proxies {
                let score = proxy.success_rate * 100.0 - proxy.speed / 10.0;
                if score > best_score {
                    best_score = score;
                    best_proxy = Some(proxy.clone());
                }
            }
        }

        best_proxy
    }

    pub async fn rotate_proxies(&self, interval_seconds: u64) {
        loop {
            sleep(Duration::from_secs(interval_seconds)).await;
            
            if let Err(e) = self.fetch_free_proxies().await {
                eprintln!("Error fetching proxies: {}", e);
            }
            
            if let Err(e) = self.test_proxies().await {
                eprintln!("Error testing proxies: {}", e);
            }
            
            println!("Proxy rotation completed");
        }
    }

    pub fn get_proxy_stats(&self) -> HashMap<String, usize> {
        let working_proxies = self.working_proxies.lock().unwrap();
        let mut stats = HashMap::new();
        
        for (country, proxies) in working_proxies.iter() {
            stats.insert(country.clone(), proxies.len());
        }
        
        stats
    }

    pub async fn validate_proxy(&self, proxy: &ProxyInfo) -> bool {
        let proxy_url = format!("http://{}:{}", proxy.ip, proxy.port);
        
        if let Ok(proxy_client) = reqwest::Client::builder()
            .proxy(Proxy::http(&proxy_url).unwrap())
            .timeout(Duration::from_secs(5))
            .build()
        {
            if let Ok(response) = proxy_client.get("http://httpbin.org/ip").send().await {
                return response.status().is_success();
            }
        }
        
        false
    }
}

#[tokio::main]
async fn main() -> Result<(), Box<dyn std::error::Error>> {
    let proxy_manager = ProxyManager::new();
    
    println!("Fetching free proxies...");
    proxy_manager.fetch_free_proxies().await?;
    
    println!("Testing proxies...");
    proxy_manager.test_proxies().await?;
    
    let stats = proxy_manager.get_proxy_stats();
    println!("Working proxies by country: {:?}", stats);
    
    if let Some(us_proxy) = proxy_manager.get_proxy_by_country("US") {
        println!("US Proxy: {}:{}", us_proxy.ip, us_proxy.port);
    }
    
    // Start continuous rotation
    proxy_manager.rotate_proxies(3600).await; // Rotate every hour
    
    Ok(())
}