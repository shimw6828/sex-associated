angular.module('sadb')
    .controller('drugController', drugController);

function drugController($scope,$http,$routeParams,sadbService) {
    var base_url = sadbService.getAPIBaseUrl();
    $scope.get_drug = function () {
        $http({
            url: base_url+'/api/get_drug_list',
            method: 'GET'
        }).then(
            function (response) {

                $scope.drug_list = response.data.drug_list;
                $scope.drug_list_count = response.data.drug_list_count
                $scope.loadcomp=true
                console.log($scope.drug_list)
            }
        )

    }
    $scope.get_drug()
    $("input").keyup(function(event){
        if(event.keyCode ==13){
             $scope.update_drug("test",1,15);
        }
    });
    $scope.update_drug = function (test,page,size) {
        var query = $('#query').val()
        console.log("ss")
        console.log(page)
        $http({
            url: base_url+'/api/get_drug_list',
            params: {query:query,page:page},
            method: 'GET'
        }).then(
            function (response) {
                console.log(response);
                $scope.drug_list = response.data.drug_list;
                $scope.drug_list_count = response.data.drug_list_count
                $scope.loadcomp=true
            }
        )
    }

}