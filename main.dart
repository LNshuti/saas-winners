import 'package:flutter/material.dart';
import 'package:charts_flutter/flutter.dart' as charts;

class MyHomePage extends StatefulWidget {
  @override
  _MyHomePageState createState() => _MyHomePageState();
}

class _MyHomePageState extends State<MyHomePage> {
  List<charts.Series> seriesList = [];
  bool loading = false;

  void _fetchData(String ticker) async {
    setState(() {
      loading = true;
    });
    final data = await fetchETFData(ticker);
    setState(() {
      // Update seriesList with the new data
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
                ElevatedButton(
                  onPressed: () => _fetchData('IVV'),
                  child: Text('Fetch ETF Data'),
                ),
              ],
            ),
    );
  }
}
