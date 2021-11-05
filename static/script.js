$(document).ready(function () {
      $('#data').DataTable({
        "searching": true,
        columns: [{"width":"20%", orderable: true, searchable: false},{"width":"70%",orderable: false, searchable: true},{"width":"10%", orderable: false, searchable: false}],
        columnDefs: [{
          render: $.fn.dataTable.render.moment('YYYY-MM-DD', 'MM/DD/YY'),
          targets: 0
        }, {}, {}]
      });
    });
