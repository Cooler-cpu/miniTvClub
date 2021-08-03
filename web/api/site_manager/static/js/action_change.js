(function($){   
    $(function(){
        $(document).ready(function() {
            // $('#id_type').bind('keyup', type_change);           
            $('.servers_archive').hide();
        });
});  
})(django.jQuery);

// based on the type, action will be loaded

var $ = django.jQuery.noConflict();

function type_change()
{
    // var action_type = $('#id_type').val();
    // $.ajax({
    //         "type"     : "GET",
    //         "url"      : "/action_choices/?action_type="+action_type,
    //         "dataType" : "json",
    //         "cache"    : false,
    //         "success"  : function(json) {
    //             $('#id_action >option').remove();
    //             for(var j = 0; j < json.length; j++){
    //                 $('#id_action').append($('<option></option>').val(json[j][0]).html(json[j][1]));
    //             }
    //         }           
    // })(jQuery);
}