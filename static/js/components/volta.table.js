/**
 * Copyright (c) 2001-present, Vonage.
 *	
 * tables (requires core)
 */

'use strict';

Volta.table = function () {	
	var _class = {
		table: 'Vlt-table',
		tall: 'Vlt-table--tall',
		short: 'Vlt-table--short',
		trigger: 'Vlt-table__density',
		buttonActive: 'Vlt-btn_active'
	}

	return {
		init: attachTableDensityHandlers
	}

	/**   
	 *	@public
	 *	
	 *	@description Attach a listener to the table density triggers
	 */
	function attachTableDensityHandlers() {
		var triggers = document.querySelectorAll('.' + _class.trigger);

		if(triggers.length > 0) {
			triggers.forEach(attachTriggerHandler);
		}

		function attachTriggerHandler(trigger) {
	      if(trigger.dataset.table) {
	        var table = document.querySelector('#' + trigger.dataset.table);

	        if(!table) {
	          console.warn('Volta: table ' + trigger.dataset.table + ' cannot be found');
	          return;
	        }

	        var activeButton = trigger.querySelector('.' + _class.buttonActive);

	        trigger.querySelectorAll('.Vlt-btn').forEach( function(button) {
	          button.addEventListener('click', function() {
	            if (this.dataset.density) {
	              console.log('in')
	              if (this.dataset.density == 'short') {
	                table.classList.add(_class.short)
	                table.classList.remove(_class.tall)
	              } else if (this.dataset.density == 'tall') {
	                table.classList.add(_class.tall)
	                table.classList.remove(_class.short)
	              } else {
	                table.classList.remove(_class.tall)
	                table.classList.remove(_class.short)
	              }

	              // update classes on buttons
	              if(activeButton) {
	                activeButton.classList.remove(_class.buttonActive);
	              }
	              activeButton = this;
	              this.classList.add(_class.buttonActive);
	            }
	          })
	        });
	      }
	    }
	}

}();