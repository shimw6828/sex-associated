angular.module('sadb')
    .controller('datasetController', datasetController);

function datasetController($scope,$http,$routeParams,sadbService) {
    var base_url = sadbService.getAPIBaseUrl();
    $scope.get_dataset = function () {
        $http({
            url: base_url+'/api/get_dataset_list',
            method: 'GET'
        }).then(
            function (response) {
                console.log(response)
                $scope.dataset_list = response.data.dataset_list;
                $scope.dataset_list_count = response.data.dataset_list_count
                $scope.loadcomp=true
                console.log($scope.dataset_list)
            }
        )

    }
    $scope.get_dataset()
    $("input").keyup(function(event){
        if(event.keyCode ==13){
             $scope.update_dataset("test",1,20);
        }
    });
    $scope.update_dataset = function (test,page,size) {
        var query = $('#query').val()
        console.log("ss")
        console.log(page)
        $http({
            url: base_url+'/api/get_dataset_list',
            params: {query:query,page:page},
            method: 'GET'
        }).then(
            function (response) {
                console.log(response);
                $scope.dataset_list = response.data.dataset_list;
                $scope.dataset_list_count = response.data.dataset_list_count
                $scope.loadcomp=true
            }
        )
    }

}