angular.module('sadb')
    .controller('geneinfoController', geneinfoController);

function geneinfoController($scope,$http,$window,$routeParams,sadbService,$sce,$anchorScroll, $location){
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
            }
        )
        $http({
            url: base_url+'/api/analysis',
            params: {gene:$routeParams.gene},
            method: 'GET'
        }).then(
            function (response) {
                $scope.analysis = response.data.analysis;
                $scope.taxname=response.data.taxname
            }
        )
        $http({
            url: base_url+'/api/get_summary',
            params: {gene:$routeParams.gene},
            method: 'GET'
        }).then(
            function (response) {
                $scope.get_summary = response.data;
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
            url: base_url+'/api/get_proteins',
            params: {gene:$routeParams.gene},
            method: 'GET'
        }).then(
            function (response) {
                $scope.proteins = response.data
            }
        )
        $http({
            url: base_url+'/api/get_phenotypes',
            params: {gene:$routeParams.gene},
            method: 'GET'
        }).then(
            function (response) {
                $scope.phenotypes = response.data
                console.log($scope.phenotypes)
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
            url: base_url+'/api/get_homolog',
            params: {gene:$routeParams.gene},
            method: 'GET'
        }).then(
            function (response) {
                $scope.homolog = response.data
            }
        )



    }
    $scope.get_gene_detail();
    $('body').scrollspy({target:'#geneInfo_siderbar',offset:90});

    $scope.goto = function (element) {
        $('html, body').animate({scrollTop:$(element).offset().top-51},100)
    }

}