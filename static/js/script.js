$(document).ready(function(){
	//Init.
	$('#addEditModal').modal({ show: false});

	// Events.
	$('#upload input[type=file]').on('change', uploadCSVFile);
	$('#add-btn').on('click', addProduct);
	$('.edit-btn').on('click', editProductInfo);
	$('.delete-btn').on('click', deleteProductInfo);
	$('#addEditModal .save-btn').on('click', saveProductInfo);

});

// Add a new Product.
function addProduct(event){
	var productInputs = $('#addEditModal .product-info input, #addEditModal .product-info textarea');
	productInputs[0].value = "";
	productInputs[1].value = "";
	productInputs[2].value = "";
	$(productInputs[0]).attr('readonly', false).attr('disabled', false);
	$('#addEditModal .addEditModal-title').text('Add Product');
	$('#addEditModal').modal('show');
}

// Remove the record from DB.
function deleteProductInfo(event){
	var productInfo = $(event.currentTarget).parent().siblings();
	if(confirm(`Remove '${$(productInfo[1]).text()}' product ?`)){
		var productData = new FormData();
		productData.append('name', $(productInfo[1]).text());
		productData.append('sku', $(productInfo[2]).text());
		$.ajax({
			headers: {
				'X-CSRF-TOKEN': $('meta[name="csrf-token"]').attr('content')
			},
			data: productData,
			type: 'DELETE',
			url: '/api/product/' + $(productInfo[2]).text(),
			processData: false,
			cache: false,
			contentType: false,
			success: function(){
				window.location.reload();
			},
			error: function(response, status, xhr){
				console.log(response, status, xhr);
			}
		});

	}
}

// Allow editing for only Product's name, description.
function editProductInfo(event){
	var productInfo = $(event.currentTarget).parent().siblings();
	var productInputs = $('#addEditModal .product-info input, #addEditModal .product-info textarea');
	productInputs[0].value = $(productInfo[2]).text();	// SKU.
	productInputs[1].value = $(productInfo[1]).text();	// Name.
	productInputs[2].value = $(productInfo[3]).text();	// Description.
	$(productInputs[0]).attr('readonly', true).attr('disabled', true);
	$('#addEditModal .addEditModal-title').text('Edit Product');
	$('#addEditModal').modal('show');
}

// Save the products info, send 'POST/PUT' request.
function saveProductInfo(){
	var productInputs = $('#addEditModal .product-info input, #addEditModal .product-info textarea');
	var productData = new FormData();
	productData.append('csrf_token', $('meta[name=csrf-token]').attr('content'));
	productData.append('name', $(productInputs[1]).val());
	productData.append('sku', $(productInputs[0]).val());
	productData.append('description', $(productInputs[2]).val());

	var requestType = 'POST';
	var requestUrl = '/api/product';
	if($('#addEditModal .addEditModal-title').text() == 'Edit Product'){
		requestType = 'PUT';
		requestUrl = requestUrl +  '/' + $(productInputs[0]).val();
	}
	$.ajax({
		data: productData,
		type: requestType,
		url: requestUrl,
		processData: false,
		cache: false,
		contentType: false,
		success: function(response, status, xhr) {
			window.location.reload();
		},
		error: function(response, status, xhr){
			console.log(response, status, xhr);
			$('#addEditModal .error-msg').text(status + '! ' + response.responseJSON.description);
		}
	});
}

// Send a POST request to Product import on uploading a new csv file.
function uploadCSVFile(event){
	var csvFile = event.currentTarget.files[0];

	// Frontend Validation for vaild filetype.
	if(!(/\.(csv)$/i).test(csvFile.name)){
        let msg = 'Please upload a valid csv file';
    }
    var csvData = new FormData();
    csvData.append('csrf_token', $('meta[name=csrf-token]').attr('content'));
	csvData.append('csv', csvFile);
    $.ajax({
    	data: csvData,
    	type: 'POST',
    	url: '/api/product-import',
    	processData: false,
		cache: false,
		contentType: false,
		success: function(response, status, xhr){
			window.location.reload();
		},
		error: function(response, status, xhr){
			console.log(xhr, response, status);
		}
    });
}