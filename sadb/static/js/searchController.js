angular.module('sadb')
    .controller('searchController', searchController);

function searchController($scope,$http,$routeParams,sadbService) {
    var base_url = sadbService.getAPIBaseUrl();
    $scope.fetch_gene = function(){
         $http({
            url: base_url+'/api/search',
            params: {gene_id:$routeParams.query},
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
        var min=$('#min').val();
        var max=$('#max').val()
         $http({
            url: base_url+'/api/search',
            params: {gene_id:$routeParams.query,page:page,min:min,max:max},
            method: 'GET'
        }).then(
            function (response) {
                $scope.gene_list = response.data.gene_list;
                $scope.gene_list = response.data.gene_list;
            }
        )}
    }




