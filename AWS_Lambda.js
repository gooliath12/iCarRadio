console.log('Loading event');
exports.handler = function(event, context) {
  var AWS = require('aws-sdk');
  var sns = new AWS.SNS();
  var ml = new AWS.MachineLearning();
  var endpointUrl = 'https://realtime.machinelearning.us-east-1.amazonaws.com';
  var mlModelId = 'ml-PHdo4dhpt9D';
  var snsTopicArn = 'arn:aws:sns:us-east-1:965479193052:iCarRadio';
  var snsMessageSubject = 'AML Prediction Result';
  var numMessagesToBeProcessed = event.Records.length;
  console.log("Number of data points to be processed:"+numMessagesToBeProcessed);
  var ml_result = {};

  var updateSns = function(result_data) {
    var params = {};
    params['TopicArn'] = snsTopicArn;
    params['Subject']  = snsMessageSubject;
    params['Message']  = result_data;
    console.log('Calling Amazon SNS to publish.');
    sns.publish(
      params,
      function(err, data) {
        if (err) {
          console.log(err, err.stack); // an error occurred
          context.done(null, 'Failed when publishing to SNS');
        }
        else {
          context.done(null, 'Published to SNS');
        }
      }
      );
  }

  var callPredict = function(input){
    console.log('calling predict');
    // AML MODEL #1
    ml.predict(
      {
        Record : input,
        PredictEndpoint : endpointUrl,
        MLModelId: mlModelId
      },
      function(err, data) {
        if (err) {
          console.log(err);
          context.done(null, 'Call to predict service failed.');
        }
        else {
          console.log('Predict call succeeded');
          ml_result['model 1'] = data.Prediction.predictedValue;
          console.log(ml_result['model 1']);
        }
      }
      );
      // AML MODEL #2
      ml.predict(
        {
          Record : input,
          PredictEndpoint : endpointUrl,
          MLModelId: mlModelId
        },
        function(err, data) {
          if (err) {
            console.log(err);
            context.done(null, 'Call to predict service failed.');
          }
          else {
            console.log('Predict call succeeded');
            console.log(data.Prediction['predictedValue']);
            ml_result['model 2'] = data.Prediction['predictedValue'];
            console.log(ml_result['model 2']);
          }
        }
        );

        updateSns(ml_result);

  }

    var processRecords = function(){
        for(i = 0; i < numMessagesToBeProcessed; ++i) {
          encodedPayload = event.Records[i].kinesis.data;
          // Amazon Kinesis data is base64 encoded so decode here
          payload = new Buffer(encodedPayload, 'base64').toString('utf-8');
          console.log("payload:"+payload);
          try {
            parsedPayload = JSON.parse(payload);
            callPredict(parsedPayload);
          }
          catch (err) {
            console.log(err, err.stack);
            context.done(null, "failed payload"+payload);
          }
        }
      }

  var checkRealtimeEndpoint = function(err, data){
      // Check ML Model's Realtime Endpoint,
      // call processRecords() function.
    if (err){
      console.log(err);
      context.done(null, 'Failed to fetch endpoint status and url.');
    }
    else {
      var endpointInfo = data.EndpointInfo;

      if (endpointInfo.EndpointStatus === 'READY') {
        endpointUrl = endpointInfo.EndpointUrl;
        console.log('Fetched endpoint url :'+endpointUrl);
        processRecords();
      } else {
        console.log('Endpoint status : ' + endpointInfo.EndpointStatus);
        context.done(null, 'End point is not Ready.');
      }
    }
  }

  ml.getMLModel({MLModelId:mlModelId}, checkRealtimeEndpoint);
};
