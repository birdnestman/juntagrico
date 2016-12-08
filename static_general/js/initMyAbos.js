
define([], function () {
	$('#filter-table thead th').each( function () {
	var title = $(this).text();
	$(this).append( '<p/><input type="text" placeholder="" style="width: 100%;" />' );
	} );

	var table = $('#filter-table').DataTable( {
	"paging":   false,
	"info":     false,
	"search": {
		"regex": true,
		"smart": false
  	},
	"drawCallback": function( settings ) {
		// do not like this but it works so far till i get around to find the correct api call
			updateSendEmailButton($('#filter-table tr').size()-2);
		}
	});

	function updateSendEmailButton(count) {
		if (count == 0) {
		    $("button#send-email")
			.prop('disabled', true)
			.text("Email senden");
		} else if (count == 1) {
		    $("button#send-email")
			.prop('disabled', false)
			.text("Email an diesen Loco senden");
		} else {
		    $("button#send-email")
			.prop('disabled', false)
			.text("Email an diese " + count + " Locos senden");
		}
	}

	table.columns().every( function () {
		var that = this;
		$( 'input', this.header() ).on( 'keyup change', function () {
		    	if ( that.search() !== this.value ) {
				that
				    .search( this.value )
				    .draw();
		    		}
		} );
	} );

	// Move the "Send email" button (and the corresponding form) to the same level as the filter input
	$("form#email-sender").appendTo("#filter-table_header div:first-child");


	$("form#email-sender").submit(function( event ) {
		var emails = [];
		$("#filter-table").find("tr").each(function () {
			var txt = $("td:eq(6)", this).text().trim();
			if (txt.length > 0) {
				// Each Abo might have a comma-separated list of email addresses
				multiple_emails = txt.split(",");
				for (var i = multiple_emails.length - 1; i >= 0; i--) {
					emails.push(multiple_emails[i].trim());
				}
			}
		});
		var abo_count = $("#filter-table").find("tr").length - 1;
		var email_count = emails.length;
		$("#recipient_type_detail").val("Sie entsprechen die Haupt- und Mitinhaber von " +
		    abo_count +
		    " Abos.");
		$("#recipients").val(emails.join("\n"));
		$("#recipients_count").val(email_count);
		$("#filter_value").val($("#filter-table_search").val());
		return;
	});
});
