(function(){

	// Constructor method
	this.CsvToTable_1 = function(){
		this.csvFile = null;

		// Create options by extending defaults with the passed in arugments
    	if (arguments[0] && typeof arguments[0] === "object") {
      		this.options = arguments[0];
    	}

	}

	CsvToTable_1.prototype.run = function() {
		return buildTable.call(this);
	}

	function getCSV() {
		try{
			var csvfile = this.options.csvFile;
			return new Promise(function(resolve, reject) {
				var request = new XMLHttpRequest();
				request.open("GET", csvfile, true);
				request.onload = function() {
				    if (request.status == 200) {
				        resolve(request.response);
				    } else {
				        reject(Error(request.statusText));
				    }
				};

				request.onerror = function() {
				 	reject(Error('Error fetching data.'));
				};
				request.send();
			});
		}catch(err){
			console.error(err);
		}
	}

    function isNotEmpty(row) {
        return row !== "";
    }

    // polyfill `.filter()` for ECMAScript <5.1
    // `f` must be pure (not modify original array).
    if (!Array.prototype.filter) {
      Array.prototype.filter = function(f) {
        "use strict";
        var p = arguments[1];
        var o = Object(this);
        var len = o.length;
        for (var i = 0; i < len; i++) {
          if (i in o) {
              var v = o[i];
              f.call(p, v, i, o);
          }
        }

        return this;
      };
    }

	function buildTable() {
		getCSV.call(this).then(function(response){
			var allRows = response.split(/\r?\n|\r/).filter(isNotEmpty);
	        var table = '<table class="table"><thead><th>Новость</th><th>Дата</th><th>Комментарии</th><th>Тональность по ключевым словам</th></thead><tbody>';

	        for (var singleRow = 1; singleRow < allRows.length; singleRow++) {
	            
	            table += '<tr>';
	            
	            var rowCells = allRows[singleRow].split(';');
				
				table += '<td>';

				table += '<details class="details"><summary class="summary"><a class ="lnk" href = "';
				table += rowCells[3];
				table +='">';
				table += rowCells[0];
				table +='</a> </summary>';
				table += rowCells[1];
				table += '</details>';
				table += '</td>';

				table += '<td>';
				table += rowCells[2];
				table += '</td>';

				table += '<td>';
				table += rowCells[4];
				table += '</td>';

				table += '<td>';
				if (rowCells[6]!==undefined && rowCells[6]!==null){
				table += '<details> <summary class = "summary">';
				table += rowCells[6];
				table +='</summary>';
				table += rowCells[5];
				table +='</details>';
				}
				table += '</td>';

				table += '</tr>';
	            
	        }
	        table += '</tbody>';
	        table += '</table>';

	        document.body.innerHTML += table;
		}, function(error){
			console.error(error);
		});
	}
}());