$(document).ready(function(){
   $(".btnSlet").click(function(){ // Click to only happen on announce links
    id=$(this).data('id');
    console.log(id)
     $('#sletBidModal').modal('show');
   $('#btn_ja_slet_bud').attr("href", "/slet_bud/"+id)
   });
});