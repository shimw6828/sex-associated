angular.module('sadb')
    .controller('browsegeneController', browsegeneController);

function browsegeneController($scope,$http,$routeParams,sadbService) {
    var base_url = sadbService.getAPIBaseUrl();
        $scope.taxons= [{ Taxonomy_Id: 9606, Scientific_name: 'Homo_sapiens',Common_name :"Human" },
                   {Taxonomy_Id: 10090, Scientific_name: 'Mus_musculus',Common_name :"Mouse" },
                   {Taxonomy_Id: 9031, Scientific_name: 'Gallus_gallus',Common_name :"Chicken" },
                    {Taxonomy_Id: 10116, Scientific_name: 'Rattus_norvegicus',Common_name :"Rat" },
                   {Taxonomy_Id: 9940, Scientific_name: 'Ovis_aries',Common_name :"Sheep" },
                    {Taxonomy_Id: 7227, Scientific_name: 'Drosophila_melanogaster',Common_name :"Fruitfly" },
                    {Taxonomy_Id: 6239, Scientific_name: 'Caenorhabditis_elegans',Common_name :"Worm" },
                    {Taxonomy_Id: 8839, Scientific_name: 'Anas_platyrhynchos',Common_name :"Duck" },
                    {Taxonomy_Id: 9103, Scientific_name: 'Meleagris_gallopavo',Common_name :"Turkey" },
                    {Taxonomy_Id: 9258, Scientific_name: 'Ornithorhynchus_anatinus',Common_name :"Platypus" },
                    {Taxonomy_Id: 13616, Scientific_name: 'Monodelphis_domestica',Common_name :"Opossum" }];
        $scope.padjs=[0.05,0.01,0.001,0.0001]
        // $scope.log2fs=[1,2,4,8]
        $http({
                url: base_url+'/api/tissue',
                method: 'GET'
            }).then(
                function (response) {
                    console.log()
                    $scope.tissues = response.data
                }
            )
    tissue=""
    stage=""
    taxon_id=""

        $scope.taxonclick = function (species) {
            taxon_id=species.Taxonomy_Id
            console.log(taxon_id)
            console.log("ok")
            $http({
                url: base_url+'/api/clickfilter',
                params: {taxon_id:taxon_id,tissue:tissue,stage:stage},
                method: 'GET'
            }).then(
                function (response) {
                    $scope.tissues = response.data.tissue
                    $scope.taxons_id = response.data.taxons
                    console.log($scope.taxons_id)
                    console.log($scope.tissues)
                    $scope.stages = response.data.stage
                    $scope.taxons= $scope.taxons.filter(item => $scope.taxon_id.indexOf(item.Taxonomy_Id.toString())!=-1)


                }
            )
            }
        $scope.tissueclick = function (ti) {
            tissue= ti
            console.log(ti)
            $http({
                url: base_url+'/api/clickfilter',
                params: {taxon_id:taxon_id,tissue:tissue,stage:stage},
                method: 'GET'
            }).then(
                function (response) {
                    $scope.tissues = response.data.tissue
                    $scope.taxon_id = response.data.taxons
                    console.log($scope.taxon_id)
                    $scope.taxons= $scope.taxons.filter(item => $scope.taxon_id.indexOf(item.Taxonomy_Id.toString())!=-1)
                    $scope.stages = response.data.stage
                    console.log($scope.taxons)
                }
            )
            }
            $scope.stageclick = function (mm) {
            console.log(mm)
            stage= mm
            $http({
                url: base_url+'/api/clickfilter',
                params: {taxon_id:taxon_id,tissue:tissue,stage:stage},
                method: 'GET'
            }).then(
                function (response) {
                    $scope.tissues = response.data.tissue
                    $scope.taxons_id = response.data.taxons
                    $scope.taxons= $scope.taxons.filter(item => $scope.taxon_id.indexOf(item.Taxonomy_Id.toString())!=-1)
                    $scope.stages = response.data.stage
                    console.log($scope.tissues)
                }
            )
            }


    $scope.loadcomp_l=true
    $scope.stages=["unknown","adult","child","larva","embryo","fetus"]
    $scope.nowloading=function () {
        $scope.loadcomp_l=false
        $scope.loadcomp_t=false
    }
    $scope.filter_gene_list = function () {
            log2_min=$('#log2_min').val();
            log2_max=$('#log2_max').val()
        padj=$('#padj span[ng-transclude]').text()
        console.log(padj)

        $http({
            url: base_url+'/api/filter',
            params: {taxon_id:taxon_id,tissue:tissue,stage:stage,log2_min:log2_min,log2_max:log2_max, padj:padj},
            method: 'GET'
        }).then(
            function (response) {
                $scope.gene_list = response.data.gene_list
                $scope.gene_list_count=response.data.gene_list_count
                console.log(response)
                $scope.loadcomp_t=true
                $scope.loadcomp_l=true
            }
        )
    }
    $scope.update_filter=function (test,page,size) {
        $http({
            url: base_url+'/api/filter',
            params: {taxon_id:taxon_id,tissue:tissue,stage:stage,log2_min:log2_min,log2_max:log2_max, padj:padj,page:page},
            method: 'GET'
        }).then(
            function (response) {
                $scope.gene_list = response.data.gene_list
                $scope.gene_list_count=response.data.gene_list_count
                console.log(response)
                $scope.loadcomp_t=true
                $scope.loadcomp_l=true
            }
        )
    }





}