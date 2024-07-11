import 'dart:convert';
import 'package:flutter/material.dart';
import 'package:http/http.dart' as http;
import 'package:charts_flutter/flutter.dart' as charts;
import 'package:posthog_flutter/posthog.dart';
import 'config.dart';

// Configuration for ETF tickers and their expense ratios
const Map<String, String> ETF_TICKERS = {
  'iShares Core S&P 500 ETF': 'IVV',
  'iShares Core S&P Total U.S. Stock Market ETF': 'ITOT',
  'iShares Core S&P Small-Cap ETF': 'IJR',
  'iShares Core MSCI Emerging Markets ETF': 'IEMG',
  'iShares Core MSCI EAFE ETF': 'IEFA',
  'iShares Core U.S. Aggregate Bond ETF': 'AGG',
  'iShares Core S&P Mid-Cap ETF': 'IJH',
  'iShares Core Dividend Growth ETF': 'DGRO',
  'iShares Core Total USD Bond Market ETF': 'IUSB',
  'iShares Russell 1000 ETF': 'IWB',
  'iShares Russell 2000 ETF': 'IWM'
};

const Map<String, double> ETF_FEES = {
  'iShares Core S&P 500 ETF': 0.03,
  'iShares Core S&P Total U.S. Stock Market ETF': 0.03,
  'iShares Core S&P Small-Cap ETF': 0.06,
  'iShares Core MSCI Emerging Markets ETF': 0.11,
  'iShares Core MSCI EAFE ETF': 0.07,
  'iShares Core U.S. Aggregate Bond ETF': 0.04,
  'iShares Core S&P Mid-Cap ETF': 0.05,
  'iShares Core Dividend Growth ETF': 0.08,
  'iShares Core Total USD Bond Market ETF': 0.06,
  'iShares Russell 1000 ETF': 0.15,
  'iShares Russell 2000 ETF': 0.19
};

void main() {
  Posthog().init(Config.posthogApiKey, host: Config.posthogHost);
  runApp(MyApp());
}

class MyApp extends StatelessWidget {
  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      title: 'ETF Tracker',
      theme: ThemeData(
        primarySwatch: Colors.blue,
      ),
      home: MyHomePage(),
    );
  }
}

class MyHomePage extends StatefulWidget {
  @override
  _MyHomePageState createState() => _MyHomePageState();
}

class _MyHomePageState extends State<MyHomePage> {
  List<charts.Series> seriesList = [];
  bool loading = false;

  Future<Map<String, dynamic>> fetchETFData(String ticker) async {
    try {
      final response = await http.get(Uri.parse(
          'https://query1.finance.yahoo.com/v7/finance/download/$ticker?period1=0&period2=${DateTime.now().millisecondsSinceEpoch ~/ 1000}&interval=1d&events=history'));
      if (response.statusCode == 200) {
        final data = response.body.split('\n').skip(1).map((line) {
          final cells = line.split(',');
          return {
            'date': DateTime.parse(cells[0]),
            'close': double.parse(cells[4])
          };
        }).toList();
        return {'ticker': ticker, 'data': data};
      } else {
        throw Exception('Failed to load ETF data');
      }
    } catch (e) {
      print('Error fetching data for $ticker: $e');
      return null;
    }
  }

  void _trackEvent(String eventName) {
    Posthog().capture(eventName, properties: {
      'property1': 'value1',
      'property2': 'value2',
    });
  }

  void _fetchData(String etfName) async {
    _trackEvent('fetch_data');
    setState(() {
      loading = true;
    });
    final data = await fetchETFData(ETF_TICKERS[etfName]);
    setState(() {
      if (data != null) {
        seriesList = [
          charts.Series<Map<String, dynamic>, DateTime>(
            id: etfName,
            colorFn: (_, __) => charts.MaterialPalette.blue.shadeDefault,
            domainFn: (Map<String, dynamic> sales, _) => sales['date'],
            measureFn: (Map<String, dynamic> sales, _) => sales['close'],
            data: data['data'],
          )
        ];
      }
      loading = false;
    });
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: Text('ETF Tracker'),
      ),
      body: loading
          ? Center(child: CircularProgressIndicator())
          : Column(
              children: <Widget>[
                Expanded(
                  child: charts.TimeSeriesChart(
                    seriesList,
                    animate: true,
                  ),
                ),
                DropdownButton<String>(
                  hint: Text('Select ETF'),
                  onChanged: (String value) {
                    _fetchData(value);
                  },
                  items: ETF_TICKERS.keys.map((String key) {
                    return DropdownMenuItem<String>(
                      value: key,
                      child: Text(key),
                    );
                  }).toList(),
                ),
              ],
            ),
    );
  }
}
