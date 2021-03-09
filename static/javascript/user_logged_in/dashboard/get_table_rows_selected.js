var symbolsArr = []
function getSelectedDataFunction() {
  symbolsArr = $('#table_user_stock_list').DataTable().rows( { selected: true } ).data().toArray();
  console.log(symbolsArr);

  $.ajax({
    type: "POST",
    contentType: "application/json;charset=utf-8",
    url: "/delete_symbols",
    traditional: "true",
    data: JSON.stringify({symbolsArr}),
    dataType: "json",
    success: function(data){
      $(symbol_tracking_list_section).replaceWith(data)
    }
    });
}