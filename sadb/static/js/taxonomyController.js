angular.module('sadb')
    .controller('taxonomyController', taxonomyController);

function taxonomyController($scope,$http,$routeParams,sadbService) {
var base_url = sadbService.getAPIBaseUrl();
    $(function () { $("[data-toggle='tooltip']").tooltip(); });
    $scope.taxons= [{ Taxonomy_Id: 9606, Scientific_name: 'Homo_sapiens' ,geneomename:"Homo_sapiens.GRCh38.dna_sm.toplevel.fa.gz",geneome:"ftp://ftp.ensembl.org/pub/release-92/fasta/homo_sapiens/dna/",annotation:"ftp://ftp.ensembl.org/pub/release-92/gtf/homo_sapiens/",annotationname:"Homo_sapiens.GRCh38.92.gtf.gz"},
                   {Taxonomy_Id: 10090, Scientific_name: 'Mus_musculus',geneomename:"Mus_musculus.GRCm38.dna_sm.toplevel.fa.gz" ,geneome:"ftp://ftp.ensembl.org/pub/release-92/fasta/mus_musculus/dna/",annotation:"ftp://ftp.ensembl.org/pub/release-92/gtf/mus_musculus/",annotationname:"Mus_musculus.GRCm38.92.gtf.gz"},
                   {Taxonomy_Id: 9031, Scientific_name: 'Gallus_gallus' ,geneomename:"Gallus_gallus.Gallus_gallus-5.0.dna_sm.toplevel.fa.gz",geneome:"ftp://ftp.ensembl.org/pub/release-92/fasta/gallus_gallus/dna/",annotation:"ftp://ftp.ensembl.org/pub/release-92/gtf/gallus_gallus/",annotationname:"Gallus_gallus.Gallus_gallus-5.0.92.gtf.gz"},
                   {Taxonomy_Id: 10116, Scientific_name: 'Rattus_norvegicus' ,geneomename:"Rattus_norvegicus.Rnor_6.0.dna_sm.toplevel.fa.gz",geneome:"ftp://ftp.ensembl.org/pub/release-92/fasta/rattus_norvegicus/dna/",annotation:"ftp://ftp.ensembl.org/pub/release-92/gtf/rattus_norvegicus/",annotationname:"Rattus_norvegicus.Rnor_6.0.92.gtf.gz"},
                   {Taxonomy_Id: 9940, Scientific_name: 'Ovis_aries',geneomename:"Ovis_aries.Oar_v3.1.dna_sm.toplevel.fa.gz" ,geneome:"ftp://ftp.ensembl.org/pub/release-92/fasta/ovis_aries/dna/",annotation:"ftp://ftp.ensembl.org/pub/release-92/gtf/ovis_aries/",annotationname:"Ovis_aries.Oar_v3.1.92.gtf.gz"},
                    {Taxonomy_Id: 7227, Scientific_name: 'Drosophila_melanogaster',geneomename:"Drosophila_melanogaster.BDGP6.dna_sm.toplevel.fa.gz" ,geneome:"ftp://ftp.ensembl.org/pub/release-92/fasta/drosophila_melanogaster/dna/",annotation:"ftp://ftp.ensembl.org/pub/release-92/gtf/drosophila_melanogaster/",annotationname:"Drosophila_melanogaster.BDGP6.92.gtf.gz"},
                    {Taxonomy_Id: 6239, Scientific_name: 'Caenorhabditis_elegans',geneomename:"Caenorhabditis_elegans.WBcel235.dna_sm.toplevel.fa.gz" ,geneome:"ftp://ftp.ensembl.org/pub/release-92/fasta/caenorhabditis_elegans/dna/",annotation:"ftp://ftp.ensembl.org/pub/release-92/gtf/caenorhabditis_elegans/",annotationname:"Caenorhabditis_elegans.WBcel235.92.gtf.gz"},
                    {Taxonomy_Id: 8839, Scientific_name: 'Anas_platyrhynchos',geneomename:"Anas_platyrhynchos.BGI_duck_1.0.dna_sm.toplevel.fa.gz" ,geneome:"ftp://ftp.ensembl.org/pub/release-92/fasta/anas_platyrhynchos/dna/",annotation:"ftp://ftp.ensembl.org/pub/release-92/gtf/anas_platyrhynchos/",annotationname:"Anas_platyrhynchos.BGI_duck_1.0.92.gtf.gz"},
                    {Taxonomy_Id: 9103, Scientific_name: 'Meleagris_gallopavo',geneomename:"Meleagris_gallopavo.UMD2.dna_sm.toplevel.fa.gz" ,geneome:"ftp://ftp.ensembl.org/pub/release-92/fasta/meleagris_gallopavo/dna/",annotation:"ftp://ftp.ensembl.org/pub/release-92/gtf/meleagris_gallopavo/",annotationname:"Meleagris_gallopavo.UMD2.92.gtf.gz"},
                    {Taxonomy_Id: 9258, Scientific_name: 'Ornithorhynchus_anatinus',geneomename:"Ornithorhynchus_anatinus.OANA5.dna_sm.toplevel.fa.gz" ,geneome:"ftp://ftp.ensembl.org/pub/release-92/fasta/ornithorhynchus_anatinus/dna/",annotation:"ftp://ftp.ensembl.org/pub/release-92/gtf/ornithorhynchus_anatinus/",annotationname:"Ornithorhynchus_anatinus.OANA5.92.gtf.gz"},
                    {Taxonomy_Id: 13616, Scientific_name: 'Monodelphis_domestica',geneomename:"Monodelphis_domestica.monDom5.dna_sm.toplevel.fa.gz" ,geneome:"ftp://ftp.ensembl.org/pub/release-92/fasta/monodelphis_domestica/dna/",annotation:"ftp://ftp.ensembl.org/pub/release-92/gtf/monodelphis_domestica/",annotationname:"Monodelphis_domestica.monDom5.92.gtf.gz"}];

    $scope.taxonomy= $scope.taxons.filter(item => item.Taxonomy_Id == $routeParams.taxonomy)[0]

    $scope.get_taxon = function () {
        console.log($routeParams.taxonomy)
        $http({
            url: base_url+'/api/taxonomy_list',
            params: {taxon_id:$routeParams.taxonomy},
            method: 'GET'
        }).then(
            function (response) {
                console.log(response)
                $scope.sagd_list_count = response.data.sagd_list_count;
                $scope.sagd_list = response.data.sagd_list;
                $scope.Scientific_name=$scope.sagd_list[1].Scientific_name.replace(" ","_")
                $scope.specie=$scope.sagd_list[1]

            }
        )
    };
    $scope.get_taxon();
    $("input").keyup(function(event){
        if(event.keyCode ==13){
             $scope.update_taxon("test",1,15);
        }
    });


    $scope.update_taxon = function (test,page,size,sort) {
        // console.log(sort)
        // if ($scope.gene_list_count<15)
        // {var filter_search = $('#filter_search_2').val();
        //  $('#filter_search').val("");
        //  $('#min').val("");
        //  var min=$('#min').val();
        //  $('#max').val("");
        //  var max=$('#max').val();}
        // else
        // {var filter_search = $('#filter_search').val();
        // var min=$('#min').val();
        // var max=$('#max').val()}
        //
        // console.log(filter_search)
        // console.log(typeof(min))
        // console.log(max)
        $http({
            url: base_url+'/api/taxonomy_list',
            params: {taxon_id:$routeParams.taxonomy,page:page},
            method: 'GET'
        }).then(
            function (response) {
                $scope.sagd_list_count = response.data.sagd_list_count;
                $scope.sagd_list = response.data.sagd_list;
                console.log($scope.sagd_list)
            }
        )
    };

}
