exports.handler = function(event, context) {
  console.log(JSON.stringify(event));

  var AWS = require('aws-sdk');
  var async = require('async');
  var sns = new AWS.SNS();
  var ml = new AWS.MachineLearning();

  // ML Model 1:  energy
  var endpointUrl_1 = 'https://realtime.machinelearning.us-east-1.amazonaws.com';
  var mlModelId_1 = 'ml-icciKHp2qJo';
  // ML Model 2: acousticness
  var endpointUrl_2 = 'https://realtime.machinelearning.us-east-1.amazonaws.com';
  var mlModelId_2 = 'ml-bFTiZ7ySeYr';
  // ML Model 3: danceability
  var endpointUrl_3 = 'https://realtime.machinelearning.us-east-1.amazonaws.com';
  var mlModelId_3 = 'ml-x9UMZPzKLHi';
  // ML Model 4: valence
  var endpointUrl_4 = 'https://realtime.machinelearning.us-east-1.amazonaws.com';
  var mlModelId_4 = 'ml-Q6hI5WdPaQM';
  
  var snsTopicArn = 'arn:aws:sns:us-east-1:965479193052:iCarRadio';
  var snsMessageSubject = 'AML Prediction Result';
  var numMessagesToBeProcessed = event.Records.length;
  console.log("Number of data points to be processed:"+numMessagesToBeProcessed);
  var ml_result = {};

  var afterML = function() {
      console.log("Print Machine Learning result:");
      console.log(ml_result);
  };

//   var updateSns = function(result_data) {
//     var params = {};
//     params['TopicArn'] = snsTopicArn;
//     params['Subject']  = snsMessageSubject;
//     params['Message']  = JSON.stringify(result_data);
//     console.log("Data prepared to be sent:" + params['Message']);
//     console.log('Calling Amazon SNS to publish.');
//     sns.publish(
//       params,
//       function(err, data) {
//         if (err) {
//           console.log(err, err.stack); // an error occurred
//           context.done(null, 'Failed when publishing to SNS');
//         }
//         else {
//           context.done(null, 'Published to SNS');
//         }
//       }
//       );
//   };

  var callPredict = function(input){
    console.log('calling predict');
    async.series([
        // AML MODEL #1
        function first(done) {
            console.log('1st function');
            ml.predict(
              {
                Record : input,
                PredictEndpoint : endpointUrl_1,
                MLModelId: mlModelId_1
              },
              function(err, data) {
                console.log('1st function ML callback');
                if (err) {
                  console.log(err);
                  context.done(null, 'Call to predict service failed.');
                }
                else {
                  console.log('Predict call succeeded');
                  ml_result['energy'] = data.Prediction.predictedValue;
                  console.log(ml_result['energy']);
                }
                done(null, ml_result['energy']);
              }
              );
            console.log("1st function finished.");
            // done(null, ml_result['energy']);
        },
          // AML MODEL #2
          function second(done) {
                console.log('2nd function');
                ml.predict(
                    {
                      Record : input,
                      PredictEndpoint : endpointUrl_2,
                      MLModelId: mlModelId_2
                    },
                    function(err, data) {
                      console.log("2nd function ML callback");
                      if (err) {
                        console.log(err);
                        context.done(null, 'Call to predict service failed.');
                      }
                      else {
                        console.log('Predict call succeeded');
                        ml_result['acousticness'] = data.Prediction['predictedValue'];
                        console.log(ml_result['acousticness']);
                      }
                      done(null, ml_result['acousticness']);
                    }
                );
                console.log('2nd function finished.');
                // done(null, ml_result['acousticness']);
          },
          
        // AML MODEL #3
          function third(done) {
                console.log('3rd function');
                ml.predict(
                    {
                      Record : input,
                      PredictEndpoint : endpointUrl_3,
                      MLModelId: mlModelId_3
                    },
                    function(err, data) {
                      console.log("3rd function ML callback");
                      if (err) {
                        console.log(err);
                        context.done(null, 'Call to predict service failed.');
                      }
                      else {
                        console.log('Predict call succeeded');
                        ml_result['danceability'] = data.Prediction['predictedValue'];
                        console.log(ml_result['danceability']);
                      }
                      done(null, ml_result['danceability']);
                    }
                );
                console.log('3rd function finished.');
                // done(null, ml_result['danceability']);
          },
          
        // AML MODEL #4
          function fourth(done) {
                console.log('4th function');
                ml.predict(
                    {
                      Record : input,
                      PredictEndpoint : endpointUrl_4,
                      MLModelId: mlModelId_4
                    },
                    function(err, data) {
                      console.log("4th function ML callback");
                      if (err) {
                        console.log(err);
                        context.done(null, 'Call to predict service failed.');
                      }
                      else {
                        console.log('Predict call succeeded');
                        ml_result['valence'] = data.Prediction['predictedValue'];
                        console.log(ml_result['valence']);
                      }
                      done(null, ml_result['valence']);
                    }
                );
                console.log('4th function finished.');
                // done(null, ml_result['valence']);
          },
        
        function fifth(done) {
            var params = {};
            params['TopicArn'] = snsTopicArn;
            params['Subject']  = snsMessageSubject;
            params['Message']  = JSON.stringify(ml_result);
            console.log("Data prepared to be sent:" + params['Message']);
            console.log('Calling Amazon SNS to publish.');
            sns.publish(
              params,
              function(err, data) {
                console.log("Published to SNS");
                if (err) {
                  console.log(err, err.stack); // an error occurred
                  context.done(null, 'Failed when publishing to SNS');
                }
                else {
                  context.done(null, 'Published to SNS');
                }
                done(null, null);
              }
              );
            // done(null, null);
        }
        // Send out the result
        ], function(err, results){
            console.log("Return aysnc results:" + results);
        });
  };

    var processRecords = function(){
        for(i = 0; i < numMessagesToBeProcessed; ++i) {
          encodedPayload = event.Records[i].kinesis.data;
          // Amazon Kinesis data is base64 encoded so decode here
          payload = new Buffer(encodedPayload, 'base64').toString('utf-8');
          console.log("payload:"+payload);
          try {
            parsedPayload = JSON.parse(payload);
            callPredict(parsedPayload);
            // updateSns(ml_result);
          }
          catch (err) {
            console.log(err, err.stack);
            context.done(null, "failed payload"+payload);
          }
        }
      };

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

  ml.getMLModel({MLModelId:mlModelId_1}, checkRealtimeEndpoint);
};
