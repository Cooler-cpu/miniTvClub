(function($){   
  $(function(){
      $(document).ready(function() {
		console.log("hi")
		$("select[name=fluss_pipelines]").on("change",()=>{type_change()})
		type_change()
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
			console.log(data)
			$("select[name=archive] option").each(function( index, item ) {
				if (item.innerHTML != "---------")
					item.remove()
			})
			data.forEach(item =>{
				$("select[name=archive]").append($('<option>').val(item.id).text(item.name))
			});
		}
	)
	.fail(
		function (data) {
			alert("false")
		}
	)
}