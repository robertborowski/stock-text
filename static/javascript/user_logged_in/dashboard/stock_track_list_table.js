/* Presenting the DataTable */
$(document).ready( function () {
  $('#table_user_stock_list').DataTable( {
    paging: true,
    "pageLength": 10,
    "bLengthChange": false,
    ordering: true,
    select: true
  } );
} );