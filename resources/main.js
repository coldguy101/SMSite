var app = angular.module('chatApp', []);
var server = 'http://162.243.91.83:5000'

app.controller('MessageCtrl', function($scope, $http, $timeout) {
  $scope.messages = []
  $scope.outbound = ''
  
  var getData = function() {
    $http({
      method: 'GET',
      url: server + '/getCurrentMessages'
    }).then(function success(response) {
      $scope.messages = response.data
      
      //Auto-scroll to new message
      var elem = document.getElementById('texts');
      $(elem).animate({ scrollTop:  elem.scrollHeight });
      
      $timeout(getData, 2000)
    }, function error(response) {
      console.log('Something terrible happened: ' + response.err)
    });
  }
  
  getData();
  
  $scope.submitText = function() {
    $http({
      method: 'POST',
      url: server + '/out',
      data: $.param({"to": "8302202388", "message": $scope.outbound}),
      headers: {'Content-Type': 'application/x-www-form-urlencoded'}
    }).then(function success(response) {
      console.log("Sent Message");
    }, function error(response) {
      console.log('Unable to send message: ' + response);
    });
    
    //Clear the outbound bound variable to clear contents of input box.
    $scope.outbound = '';
  }
});