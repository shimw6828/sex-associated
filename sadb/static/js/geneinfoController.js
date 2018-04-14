angular.module('sadb')
    .controller('geneinfoController', geneinfoController);

function geneinfoController($scope,$http,$window,$routeParams,sadbService,$sce){
    var base_url = sadbService.getAPIBaseUrl();
    $scope.get_gene_detail = function () {
        console.log("detail work");
        $scope.gene_id=$routeParams.gene
        $http({
            url: base_url+'/api/get_detail',
            params: {gene:$routeParams.gene},
            method: 'GET'
        }).then(
            function (response) {
                $scope.gene_detail = response.data;
                if ($scope.gene_detail.hgnc_id!="nan"){$scope.gene_detail.hgnc_id=$scope.gene_detail.hgnc_id.substr(5)}

                console.log($scope.gene_detail)
            }
        )

        $http({
            url: base_url+'/api/get_summary',
            params: {gene:$routeParams.gene},
            method: 'GET'
        }).then(
            function (response) {
                $scope.get_summary = response.data;
                console.log($scope.get_summary.synonyms)
            }
        )
        $http({
            url: base_url+'/api/get_drug_info',
            params: {gene:$routeParams.gene},
            method: 'GET'
        }).then(
            function (response) {
                $scope.get_drug_info = response.data;
            }
        )
        $http({
            url: base_url+'/api/get_gene_structures',
            params: {gene:$routeParams.gene},
            method: 'GET'
        }).then(
            function (response) {
                $scope.transcript = response.data.transcript;
                $scope.gene_model =  $sce.trustAsHtml(response.data.gene_model);
            }
        )
        $http({
            url: base_url+'/api/get_go_terms',
            params: {gene:$routeParams.gene},
            method: 'GET'
        }).then(
            function (response) {
                $scope.go_terms = response.data
            }
        )
        $http({
            url: base_url+'/api/get_homolog',
            params: {gene:$routeParams.gene},
            method: 'GET'
        }).then(
            function (response) {
                $scope.homolog = response.data
            }
        )
        $http({
            url: base_url+'/api/get_paralogue',
            params: {gene:$routeParams.gene},
            method: 'GET'
        }).then(
            function success(response) {
                $scope.paralogue = response.data
            },
            function error() {
               $scope.paralogue = 0
            }
        )
        $http({
            url: base_url+'/api/get_proteins',
            params: {gene:$routeParams.gene},
            method: 'GET'
        }).then(
            function (response) {
                $scope.proteins = response.data
            }
        )
        $http({
            url: base_url+'/api/analysis',
            params: {gene:$routeParams.gene},
            method: 'GET'
        }).then(
            function (response) {
                $scope.analysis = response.data.analysis;
                $scope.url=response.data.url
            }
        )
    }
    $scope.get_gene_detail();

}