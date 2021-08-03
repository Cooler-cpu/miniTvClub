(function($){   
  $(function(){
      $(document).ready(function() {
		let type = getSelectType()
		$("select[name=fluss_pipelines]").on("change",()=>{type_change()})
		if (type == undefined)      
			$('.servers_archive').hide();
		else{
			type_change(stream_name)
		}
      });
});  
})(django.jQuery);

var $ = django.jQuery.noConflict();


function getCSRFToken() {
    return $("input[name=csrfmiddlewaretoken]").val()
}


function getSelectType() {
	let option_id = $("select[name=fluss_pipelines]").val()
    return $("select[name=fluss_pipelines] option")[option_id].innerHTML
}


function type_change(){
    let data = {
		"csrfmiddlewaretoken": $("input[name=csrfmiddlewaretoken]").val(),
		"pipeline_name": getSelectType(),
	},
		action = location.origin + "/api/v1/get_piplines"

	$.post(
		action,
		data,
	)
	.done(
		function (data) {
			alert("try")
		}
	)
	.fail(
		function (data) {
			alert("false")
		}
	)
}