angular.module('sadb')
    .controller('testController', testController);

function testController($scope,$http,$routeParams,sadbService) {
    var base_url = sadbService.getAPIBaseUrl();
    $scope.fetch_gene = function(){
         $http({
            url: base_url+'/api/test',
            params: {gene_id:$routeParams.gene_id},
            method: 'GET'
        }).then(
            function (response) {
                console.log(response);
                $scope.gene_list_count = response.data.gene_list_count;
                $scope.gene_list = response.data.gene_list;
            }
        )
    };
    $scope.fetch_gene();
    $scope.update_gene = function(test,page,size){
        console.log(page)
         $http({
            url: base_url+'/api/test',
            params: {gene_id:$routeParams.gene_id,page:page},
            method: 'GET'
        }).then(
            function (response) {
                $scope.gene_list = response.data.gene_list;
            }
        )
    };




}