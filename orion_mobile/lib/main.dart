import 'package:flutter/material.dart';
import 'package:http/http.dart' as http;
import 'dart:convert';
import 'dart:async';

void main() => runApp(OrionApp());

class OrionApp extends StatelessWidget {
  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      title: 'Orion Monitor',
      theme: ThemeData.dark().copyWith(
        primarySwatch: Colors.blue,
        scaffoldBackgroundColor: Colors.black,
      ),
      home: OrionDashboard(),
    );
  }
}

class OrionDashboard extends StatefulWidget {
  @override
  _OrionDashboardState createState() => _OrionDashboardState();
}

class _OrionDashboardState extends State<OrionDashboard> {
  Timer? _timer;
  Map<String, dynamic> _status = {};
  Map<String, dynamic> _earnings = {};
  Map<String, dynamic> _missions = {};
  String _serverUrl = 'https://your-orion-server.com'; // Your cloud server URL
  String _webhookUrl = 'https://your-notification-service.com/webhook';

  @override
  void initState() {
    super.initState();
    _startPolling();
  }

  void _startPolling() {
    _setWebhook();
    _timer = Timer.periodic(Duration(seconds: 5), (timer) {
      _fetchData();
    });
    _fetchData();
  }

  Future<void> _setWebhook() async {
    try {
      await http.post(
        Uri.parse('$_serverUrl/api/webhook'),
        headers: {'Content-Type': 'application/json'},
        body: json.encode({'url': _webhookUrl})
      );
    } catch (e) {
      print('Error setting webhook: $e');
    }
  }

  Future<void> _fetchData() async {
    try {
      final statusResponse = await http.get(Uri.parse('$_serverUrl/api/status'));
      final earningsResponse = await http.get(Uri.parse('$_serverUrl/api/earnings'));
      final missionsResponse = await http.get(Uri.parse('$_serverUrl/api/missions'));

      if (statusResponse.statusCode == 200) {
        setState(() {
          _status = json.decode(statusResponse.body);
          _earnings = json.decode(earningsResponse.body);
          _missions = json.decode(missionsResponse.body);
        });
      }
    } catch (e) {
      print('Error fetching data: $e');
    }
  }

  Future<void> _controlSystem(String action) async {
    try {
      String endpoint = action == 'start' ? '/api/start' : '/api/stop';
      await http.post(Uri.parse('$_serverUrl$endpoint'));
      _fetchData();
    } catch (e) {
      print('Error controlling system: $e');
    }
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: Text('ORION MONITOR'),
        backgroundColor: Colors.blue[900],
      ),
      body: RefreshIndicator(
        onRefresh: _fetchData,
        child: ListView(
          padding: EdgeInsets.all(16),
          children: [
            _buildStatusCard(),
            SizedBox(height: 16),
            _buildEarningsCard(),
            SizedBox(height: 16),
            _buildMissionsCard(),
            SizedBox(height: 16),
            _buildControlPanel(),
          ],
        ),
      ),
    );
  }

  Widget _buildStatusCard() {
    return Card(
      color: Colors.grey[900],
      child: Padding(
        padding: EdgeInsets.all(16),
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            Text('SYSTEM STATUS', style: TextStyle(fontSize: 18, fontWeight: FontWeight.bold)),
            SizedBox(height: 8),
            Row(
              children: [
                Icon(
                  _status['active'] == true ? Icons.check_circle : Icons.error,
                  color: _status['active'] == true ? Colors.green : Colors.red,
                ),
                SizedBox(width: 8),
                Text(_status['active'] == true ? 'OPERATIONAL' : 'OFFLINE'),
              ],
            ),
            SizedBox(height: 8),
            Text('Sites: ${_status['sites_count'] ?? 0}'),
            Text('Active Missions: ${_status['active_missions'] ?? 0}'),
          ],
        ),
      ),
    );
  }

  Widget _buildEarningsCard() {
    return Card(
      color: Colors.grey[900],
      child: Padding(
        padding: EdgeInsets.all(16),
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            Text('EARNINGS', style: TextStyle(fontSize: 18, fontWeight: FontWeight.bold)),
            SizedBox(height: 8),
            Text('Total: \$${_earnings['total_usd']?.toStringAsFixed(2) ?? '0.00'}', 
                 style: TextStyle(fontSize: 24, color: Colors.green)),
            SizedBox(height: 8),
            Text('Today: \$${_earnings['today']?.toStringAsFixed(2) ?? '0.00'}'),
            Text('Crypto: \$${_earnings['crypto']?.toStringAsFixed(2) ?? '0.00'}'),
            Text('Gift Cards: \$${_earnings['gift_cards']?.toStringAsFixed(2) ?? '0.00'}'),
          ],
        ),
      ),
    );
  }

  Widget _buildMissionsCard() {
    return Card(
      color: Colors.grey[900],
      child: Padding(
        padding: EdgeInsets.all(16),
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            Text('MISSIONS', style: TextStyle(fontSize: 18, fontWeight: FontWeight.bold)),
            SizedBox(height: 8),
            Text('Active: ${_missions['active'] ?? 0}'),
            Text('Completed Today: ${_missions['completed_today'] ?? 0}'),
            Text('Success Rate: ${(_missions['success_rate'] ?? 0).toStringAsFixed(1)}%'),
          ],
        ),
      ),
    );
  }

  Widget _buildControlPanel() {
    return Card(
      color: Colors.grey[900],
      child: Padding(
        padding: EdgeInsets.all(16),
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            Text('CONTROL PANEL', style: TextStyle(fontSize: 18, fontWeight: FontWeight.bold)),
            SizedBox(height: 16),
            Row(
              mainAxisAlignment: MainAxisAlignment.spaceEvenly,
              children: [
                ElevatedButton(
                  onPressed: () => _controlSystem('start'),
                  child: Text('START'),
                  style: ElevatedButton.styleFrom(backgroundColor: Colors.green),
                ),
                ElevatedButton(
                  onPressed: () => _controlSystem('pause'),
                  child: Text('PAUSE'),
                  style: ElevatedButton.styleFrom(backgroundColor: Colors.orange),
                ),
                ElevatedButton(
                  onPressed: () => _controlSystem('stop'),
                  child: Text('STOP'),
                  style: ElevatedButton.styleFrom(backgroundColor: Colors.red),
                ),
              ],
            ),
          ],
        ),
      ),
    );
  }

  @override
  void dispose() {
    _timer?.cancel();
    super.dispose();
  }
}