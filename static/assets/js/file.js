		$(document).ready(function() {
			$('#time-slots-table').DataTable();
		});

		function updateAmount() {
			var num_adults = document.getElementById("num_adults").value;
			var num_children = document.getElementById("num_children").value;
			var total_amount = (num_adults * 100) + (num_children * 50);
			document.getElementById("total_amount").value = "$" + total_amount.toFixed(2);
		}