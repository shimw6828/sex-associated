angular.module('sadb')
    .controller('browseController', browseController);

function browseController($scope,$http,$routeParams,sadbService) {
    var base_url = sadbService.getAPIBaseUrl();
    var taxs=[
        {scientific_name:"Anolis carolinensis",common_name:"Anole lizard"},
        {scientific_name:"Gallus gallus",common_name:"Chicken"},
        {scientific_name:"Meleagris gallopavo",common_name:"Turkey"},
        {scientific_name:"Anas platyrhynchos",common_name:"Duck"},
        {scientific_name:"Ficedula albicollis",common_name:"Flycatcher"},
        {scientific_name:"Taeniopygia guttata",common_name:"Zebra Finch"},
        {scientific_name:"Cavia aperea",common_name:"Brazilian guinea pig"},
        {scientific_name:"Cavia porcellus",common_name:"Guinea Pig"},
        {scientific_name:"Octodon degus",common_name:"Degu"},
        {scientific_name:"Chinchilla lanigera",common_name:"Long-tailed chinchilla"},
        {scientific_name:"Fukomys damarensis",common_name:"Damara mole rat"},
        {scientific_name:"Heterocephalus glaber",common_name:"Naked mole-rat female"},
        {scientific_name:"Cricetulus griseus",common_name:"Chinese hamster CHOK1GS"},
        {scientific_name:"Mesocricetus auratus",common_name:"Golden Hamster"},
        {scientific_name:"Microtus ochrogaster",common_name:"Prairie vole"},
        {scientific_name:"Peromyscus maniculatus",common_name:"Northern American deer mouse"},
        {scientific_name:"Mus musculus",common_name:"Mouse"},
        {scientific_name:"Nannospalax galili",common_name:"Upper Galilee mountains blind mole rat"},
        {scientific_name:"Jaculus jaculus",common_name:"Lesser Egyptian jerboa"},
        {scientific_name:"Dipodomys ordii",common_name:"Kangaroo rat"},
        {scientific_name:"Ictidomys tridecemlineatus",common_name:"Squirrel"},
        {scientific_name:"Oryctolagus cuniculus",common_name:"Rabbit"},
        {scientific_name:"Otolemur garnettii",common_name:"Bushbaby"},
        {scientific_name:"Microcebus murinus",common_name:"Mouse Lemur"},
        {scientific_name:"Pan troglodytes",common_name:"Chimpanzee"},
        {scientific_name:"Homo sapiens",common_name:"Human"},
        {scientific_name:"Gorilla gorilla",common_name:"Gorilla"},
        {scientific_name:"Nomascus leucogenys",common_name:"Gibbon"},
        {scientific_name:"Macaca mulatta",common_name:"Macaque"},
        {scientific_name:"Papio anubis",common_name:"Olive baboon"},
        {scientific_name:"Chlorocebus sabaeus",common_name:"Vervet-AGM"},
        {scientific_name:"Callithrix jacchus",common_name:"Marmoset"},
        {scientific_name:"Bos taurus",common_name:"Cow"},
        {scientific_name:"Sus scrofa",common_name:"Pig"},
        {scientific_name:"Canis lupus",common_name:"Dog"},
        {scientific_name:"Ailuropoda melanoleuca",common_name:"Panda"},
        {scientific_name:"Equus caballus",common_name:"Horse"},
        {scientific_name:"Myotis lucifugus",common_name:"Microbat"},
        {scientific_name:"Loxodonta africana",common_name:"Elephant"},
        {scientific_name:"Monodelphis domestica",common_name:"Opossum"},
        {scientific_name:"Ornithorhynchus anatinus",common_name:"Platypus"},
        {scientific_name:"Xenopus tropicalis",common_name:"Xenopus"},
        {scientific_name:"Latimeria chalumnae",common_name:"Coelacanth"},
        {scientific_name:"Takifugu rubripes",common_name:"Fugu"},
        {scientific_name:"Tetraodon nigroviridis",common_name:"Tetraodon"},
        {scientific_name:"Gasterosteus aculeatus",common_name:"Stickleback"},
        {scientific_name:"Oryzias latipes",common_name:"Medaka"},
        {scientific_name:"Xiphophorus maculatus",common_name:"Platyfish"},
        {scientific_name:"Lepisosteus oculatus",common_name:"Spotted gar"},
        {scientific_name:"Petromyzon marinus",common_name:"Lamprey"},
        {scientific_name:"Ciona intestinalis",common_name:"C.intestinalis"}
    ]
    $scope.tax_list=taxs;
   //js加载过快，会使naturalWidth为0

    $('#Species').ready(function(){
        var mapD = $('area'); //获取页面所有的热点区域
        var imgW = 1378
        var imgH = 2780
        console.log(imgW,imgH,mapD.length)
        var imgW01 = $('#Species').width()
        var test = $('#Species').height()
        imgH01= 1565.190
        console.log(imgW01,test,mapD.length)
        var W_Multiple = imgW01/imgW; //对应比例
        var H_Multiple = imgH01/imgH; //对应比例
        var _arrS = ''; //存放coords的值
        var _arr = []; //存放coords对应的值
        for (var i = 0; i < mapD.length; i++) { //热点区域的个数
            _arr = [];
            _arrS = $(mapD[i]).attr('coords');
            _arr = _arrS.split(',');

            _arr[0]=_arr[0]*W_Multiple;
            _arr[1]=_arr[1]*H_Multiple;
            _arrS = _arr.join(',');
            console.log(_arrS)
            // 把缩放比例后对应的coords，赋值给原有coords
            $(mapD[i]).attr('coords',_arrS);
        }
    });
};


