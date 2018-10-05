var django = {
  "jQuery": jQuery.noConflict(true)
};
var jQuery = django.jQuery;
var $ = jQuery;

var ptx = (function ($, ptx) {
  "use strict";

  ptx.ref = (function ($, config) {
    // Define variables for ru.collbank here
    var loc_example = "",
        basket_progress = "",         // URL to get progress
        basket_stop = "",             // URL to stop the basket
        basket_result = "",           // URL to the results for this basket
        basket_data = null,           // DATA to be sent along
        /* loc_files = null, */
        oSyncTimer = null,
        loc_divErr = "ptx_err";

    // Private methods specification
    var private_methods = {
      /**
       * methodNotVisibleFromOutside - example of a private method
       * @returns {String}
       */
      methodNotVisibleFromOutside: function () {
        return "something";
      },
      errMsg: function (sMsg, ex) {
        var sHtml = "";
        if (ex === undefined) {
          sHtml = "Error: " + sMsg;
        } else {
          sHtml = "Error in [" + sMsg + "]<br>" + ex.message;
        }
        sHtml = "<code>" + sHtml + "</code>";
        $("#" + loc_divErr).html(sHtml);
      },
      errClear: function () {
        $("#" + loc_divErr).html("");
      }
    }

    // Public methods
    return {
      ajaxcall: function (sUrl, data, sMethod) {
        var response = {};

        try {
          if (sUrl === undefined || sUrl === "" || data === undefined) {
            // Cannot do anything with this, so respond with a bad status
            response['status'] = "error";
            response['msg'] = "Missing obligatory parameter(s): URL, data";
            return response;
          }
          // There is valid information, continue
          $.ajax({
            url: sUrl,
            type: sMethod,
            data: data,
            async: false,
            dataType: 'json',
            success: function (data) {
              response = data;
            },
            failure: function () {
              var iStop = 1;
            }
          });
          // Return the response
          return response;
        } catch (ex) {
          private_methods.errMsg("ajaxcall", ex);
        }
      },

      import_data: function (el) {
        var frm = null,
            targeturl = "",
            uploadurl = "",
            fdata = null,
            data = null,
            xhr = null,
            files = null,
            more = {},              // Additional (json) data
            sTargetDiv = "",
            sTestType = "gist",
            sMsg = "";

        try {

          // Get the URL
          targeturl = $(el).attr("targeturl");
          uploadurl = $(el).attr("uploadurl");
          sTargetDiv = $(el).attr("targetid");

          // Show progress
          $("#import_progress").attr("value", "0");
          $("#import_progress").removeClass("hidden");
          // Add data: 
          frm = $(el).closest("form");
          if (frm !== undefined) { data = $(frm).serializeArray(); }

          for (var i = 0; i < data.length; i++) {
            more[data[i]['name']] = data[i]['value'];
          }
          // Showe the user needs to wait...
          ptx.ref.show_waiting(true);
          // Upload XHR
          $("#id_file_source").upload(targeturl,
            more,
            function (response) {
              // Transactions have been uploaded...
              console.log("done: ", response);

              // First leg has been done
              if (response === undefined || response === null || !("status" in response)) {
                private_methods.errMsg("No status returned");
              } else {
                switch (response.status) {
                  case "ok":
                    // Remove all project-part class items
                    $(".project-part").addClass("hidden");
                    // Place the response here
                    $("#" + sTargetDiv).html(response.html);
                    $("#" + sTargetDiv).removeClass("hidden");
                    // Make sure events are in place again
                    ptx.ref.init_events();
                    break;
                  default:
                    // Show the error that has occurred
                    if ("html" in response) { sMsg = response['html']; }
                    if ("error_list" in response) { sMsg += response['error_list']; }
                    // Show that the project has finished
                    private_methods.errMsg("Execute error: " + sMsg);
                    break;
                }
              }
              ptx.ref.show_waiting(false);
            }, function (progress, value) {
              console.log(progress);
              $("#import_progress").val(value);
            }
          );
          // Hide progress after some time
          setTimeout(function () { $("#import_progress").addClass("hidden"); }, 1000);

        } catch (ex) {
          private_methods.errMsg("import_data", ex);
          ptx.ref.show_waiting(false);
        }
      },

      load_item: function (el) {
        var sUrl = "",
            sTargetDiv = "",
            sMsg = "";

        try {
          if (el === undefined || el === null) return false;
          private_methods.errClear();
          sUrl = $(el).attr("targeturl");
          sTargetDiv = $(el).attr("targetid");
          if (sUrl !== undefined && sUrl !== "" && sTargetDiv !== undefined && sTargetDiv !== "") {
            // Show we are waiting
            ptx.ref.show_waiting(true);
            $.get(sUrl, function (response) {
              sTargetDiv = "#" + sTargetDiv;
              ptx.ref.show_waiting(false);
              if (response !== undefined && response !== null) {
                if (response.status === undefined) {
                  private_methods.errMsg("No status returned");
                } else if (response.status === "error") {
                  // Show the error that has occurred
                  if ("html" in response) { sMsg = response['html']; }
                  if ("error_list" in response) { sMsg += response['error_list']; }
                  // Show that the project has finished
                  private_methods.errMsg("Execute error: " + sMsg);
                } else {
                  // Remove all project-part class items
                  $(".project-part").addClass("hidden");
                  // Place the response here
                  $(sTargetDiv).html(response.html);
                  $(sTargetDiv).removeClass("hidden");
                  // Make sure events are in place again
                  ptx.ref.init_events();
                }
              }
            });
          }
        } catch (ex) {
          private_methods.errMsg("load_item", ex);
          ptx.ref.show_waiting(false);
        }
      },

      /**
       * project_choice
       *   Process the chosen project and show the result
       *
       */
      project_choice: function (el, sTarget) {
        var divTarget = "",
            divOption = null, // Chosen <option>
            sProject = "",    // Chosen project
            sFile = "",       // Chosen file to be imported
            sHtml = "",
            iChosen = 0,      // ID of chosen one
            sChosen = "";     // Option that has been chosen

        try {
          // Get the target <div>
          divTarget = "#" + sTarget;
          // Find out what has been chosen
          sChosen = $("#select_project").val();
          sFile = $("#select_excel").val();
          if (sChosen !== undefined && sChosen !== "" && sChosen !== "-") {
            // Get the integer that has been chosen
            iChosen = parseInt(sChosen, 10);
            divOption = $("#select_project").find("option[value=" + iChosen + "]");
            if (divOption !== undefined && divOption !== null) {

              sProject = $(divOption).text();
              sHtml = "<div class='col-md-12'>" +
                "<table class='seeker-choice'>" +
                "<tr><td nowrap valign='top'>Project: </td><td class='b' valign='top'>" + sProject + "</td></tr>" +
                "<tr><td nowrap valign='top'>Excel file:</td><td class='b' valign='top'>" + sFile + "</td></tr>" +
                "</table></div>";
              $(divTarget).html(sHtml);

              // TODO: Check whether this search has already been made
            }
          }

        } catch (ex) {
          private_methods.errMsg("project_choice", ex);
        }
      },

      /**
       *  init_events
       *      Bind main necessary events
       *
       */
      init_events: function () {
        var sExcelInput = "D:/Data Files/Private/Mangoboom/finance/Boekhouding/2017/Boekhouding2017_Dec-versie02.xlsm";

        try {
          var sFileDiv = $("#select_excel");
          if (sFileDiv !== undefined && sFileDiv.length > 0) {
            $(sFileDiv).val(sExcelInput);
          }
          $('tr.add-row a').click(ptx.ref.tabular_addrow);
          $('.inline-group > div > a.btn').click(function () {
            var elGroup = null,
                elTabular = null,
                sStatus = "";

            // Get the tabular
            elTabular = $(this).parent().next(".tabular");
            if (elTabular !== null) {
              // Get the status of this one
              if ($(elTabular).hasClass("hidden")) {
                $(elTabular).removeClass("hidden");
              } else {
                $(elTabular).addClass("hidden");
              }
            }
          });
          $('span.td-toggle-textarea').unbind('click').click(ptx.ref.toggle_textarea_click);
          $('input.td-toggle-textarea').unbind('click').click(ptx.ref.toggle_textarea_click);
          // Make sure variable ordering is supported
          $('td span.var-down').unbind('click').click(ptx.ref.var_down);
          $('td span.var-up').unbind('click').click(ptx.ref.var_up);

          // Allow form-row items to be selected or unselected
          $('tr.form-row').each(function () {
            // Add it to the first visible cell
            $(this).find("td").not(".hidden").first().unbind('click').click(ptx.ref.form_row_select);
            // Make sure any other cells  that have an <input> or a <td-toggle-textarea> are set too
            $(this).find("td").not(".hidden").each(function () {
              if ($(this).find("input").length > 0 ||
                  $(this).find("span.td-toggle-textarea").length > 0) {
                $(this).unbind("click").click(ptx.ref.form_row_select);
              }
            });
          });

          // Make sure all <input> elements in a <form> are treated uniformly
          $("form input[type='text']").each(function () {
            var $this = $(this),
                $span = $this.prev("span");
            // Create span if not existing
            if ($span === undefined || $span === null || $span.length === 0) {
              $span = $this.before("<span></span");
              // Still need to go to the correct function
              $span = $this.prev("span");
            }
            // Set the value of the span
            $span.html($this.val());
            // Now specify the action on clicking the span
            $span.on("click", function () {
              var $this = $(this);
              $this.hide().siblings("input").show().focus().select();
            });
            // Specify what to do on blurring the input
            $this.on("blur", function () {
              var $this = $(this);
              // Show the value of the input in the span
              $this.hide().siblings("span").text($this.val()).show();
            }).on("keydown", function (e) {
              // SPecify what to do if the tab is pressed
              if (e.which === 9) {
                e.preventDefault();
                if (e.shiftKey) {
                  // Need to go backwards
                  $(this).blur().closest("tr").prev("tr").find("input[type='text']").not(".hidden").first().prev("span").click();
                } else {
                  // Move forwards
                  $(this).blur().closest("tr").next("tr").find("input[type='text']").not(".hidden").first().prev("span").click();
                }
              }
            });
            // Make sure the <input> is hidden, unless it is empty
            if ($this.val() !== "") {
              $this.hide();
            }
          });

          // NOTE: do not use the following mouseout event--it is too weird to work with
          // $('td span.td-textarea').mouseout(ptx.ref.toggle_textarea_out);

          // Bind the click event to all class="ajaxform" elements
          $(".ajaxform").unbind('click').click(ptx.ref.ajaxform_click);

        } catch (ex) {
          private_methods.errMsg("init_events", ex);
        }
      },

      /**
       * import_start
       *   Start importing
       *
       */
      import_start(elStart) {
        var sDivProgress = "#import_progress",
            ajaxurl = "",
            response = null,
            project_id = -1,
            frm = null,
            sMsg = "",
            data = [];


        try {
          // Clear the errors
          private_methods.errClear();

          // obligatory parameter: ajaxurl
          ajaxurl = $(elStart).attr("ajaxurl");

          // Gather the information
          frm = $(elStart).closest("form");
          if (frm !== undefined) { data = $(frm).serializeArray(); }

          // Make an AJAX call to start the import
          response = ptx.ref.ajaxcall(ajaxurl, data, "POST");
          if (response.status === undefined) {
            // Show an error somewhere
            private_methods.errMsg("Bad import response");
            $(sDivProgress).html("Bad import response:<br>" + response);
          } else if (response.status === "error") {
            // Show the error that has occurred
            if ("html" in response) { sMsg = response['html']; }
            if ("error_list" in response) { sMsg += response['error_list']; }
            private_methods.errMsg("Import error: " + sMsg);
            $(sDivProgress).html("import error");
          } else {
            // All went well -- get the basket id
            basket_id = response.basket_id;
            basket_progress = response.basket_progress;
            basket_stop = response.basket_stop;
            basket_result = response.basket_result;
            basket_data = data;

            // Start the next call for status after 1 second
            setTimeout(function () { ptx.ref.import_progress(); }, 1000);
          }

        } catch (ex) {
          private_methods.errMsg("import_start", ex);
        }

      },

      /**
       * import_progress
       *   Elicit and show the status of an ongoing search
       *
       */
      import_progress() {
        var sDivProgress = "#import_progress",
            response = null,
            html = [],
            sMsg = "";

        try {
          // Make an AJAX call by using the already stored basket_stop URL
          response = ptx.ref.ajaxcall(basket_progress, basket_data, "POST");
          if (response.status !== undefined) {
            if ('html' in response) { sMsg = response.html; }
            switch (response.status) {
              case "ok":
                // Action depends on the statuscode
                switch (response.statuscode) {
                  case "working":
                    // Show the status of the project
                    $(sDivProgress).html(response.html);
                    // Make sure we are called again
                    setTimeout(function () { ptx.ref.import_progress(); }, 500);
                    break;
                  case "completed":
                  case "finished":
                    // Show that the project has finished
                    $(sDivProgress).html(response.html);
                    break;
                  case "error":
                    // THis is an Xquery error
                    // Show that the project has finished
                    $(sDivProgress).html("Sorry, but there is an error");
                    // Do NOT shoe the RESULTS button
                    break;
                  default:
                    // Show the current status
                    private_methods.errMsg("Unknown statuscode: [" + response.statuscode + "]");
                    break;
                }
                break;
              case "error":
                if ('error_list' in response) { sMsg += response.error_list; }
                private_methods.errMsg("Progress error: " + sMsg);
                break;
            }
          }

        } catch (ex) {
          private_methods.errMsg("import_progress", ex);
        }
      },

      /**
       * nowTime
       *   Get the current time as a string
       *
       */
      nowTime: function () {
        var now = new Date(Date.now());
        var sNow = now.getHours() + ":" + now.getMinutes() + ":" + now.getSeconds();
        return sNow;
      },

      show_waiting: function (bShow) {
        var elWaiting = "#waiting";

        try {
          if (bShow) {
            $(elWaiting).removeClass("hidden")
          } else {
            $(elWaiting).addClass("hidden");
          }

        } catch (ex) {
          private_methods.errMsg("show_waiting", ex);
        }
      },

      /**
       *  sync_start
       *      Start synchronisation
       *
       */
      sync_start: function (sSyncType, object_id) {
        var oJson = {},
            oData = {},
            i,
            sParam = "",
            arKV = [],
            arParam = [],
            sUrl = "";

        // Indicate that we are starting
        $("#sync_progress_" + sSyncType).html("Synchronization is starting: " + sSyncType);

        // Make sure that at the end: we stop
        oData = { 'type': sSyncType };
        // More data may be needed for particular types
        switch (sSyncType) {
          case "journal":
            // Retrieve the parameters from the <form> settings
            sParam = $("#sync_form_" + sSyncType).serialize();
            arParam = sParam.split("&");
            for (i = 0; i < arParam.length; i++) {
              arKV = arParam[i].split("=");
              // Store the parameters into a JSON object
              oData[arKV[0]] = arKV[1];
            }
            break;
        }

        // Start looking only after some time
        oJson = { 'status': 'started' };
        ptx.ref.oSyncTimer = window.setTimeout(function () { ptx.ref.sync_progress(sSyncType, oJson); }, 3000);

        // Define the URL
        sUrl = $("#sync_start_" + sSyncType).attr('sync-start');
        // Perform a request to get started
        $.get(sUrl, oData, function (response) {
          $("#sync_details_" + sSyncType).html("start >> sync_stop");
          ptx.ref.sync_stop(sSyncType, json);
        }).failure(function (response) {
          $("#sync_details_" + sSyncType).html("Ajax failure");
        });
      },

      /**
       *  sync_progress
       *      Return the progress of synchronization
       *
       */
      sync_progress: function (sSyncType, options) {
        var oData = {},
            sUrl = "";

        oData = { 'type': sSyncType };
        sUrl = $("#sync_start_" + sSyncType).attr('sync-progress');

        $.get(sUrl, oData, function (response) {
          $("#sync_details_" + sSyncType).html("progress >> sync_handle");
          ptx.ref.sync_handle(sSyncType, response);
        }).failure(function (response) {
          $("#sync_details_" + sSyncType).html("Ajax failure");
        });
      },

      /**
       *  sync_handle
       *      Process synchronisation
       *
       */
      sync_handle: function (sSyncType, json) {
        var sStatus = "",
            options = {};

        // Validate
        if (json === undefined) {
          sStatus = $("#sync_details_" + sSyncType).html();
          $("#sync_details_" + sSyncType).html(sStatus + "(undefined status)");
          return;
        }
        // Action depends on the status in [json]
        switch (json.status) {
          case 'error':
            // Show we are ready
            $("#sync_progress_" + sSyncType).html("Error synchronizing: " + sSyncType);
            $("#sync_details_" + sSyncType).html(ptx.ref.sync_details(json));
            // Stop the progress calling
            window.clearInterval(ptx.ref.oSyncTimer);
            // Leave the routine, and don't return anymore
            return;
          case "done":
          case "finished":
            // Default action is to show the status
            $("#sync_progress_" + sSyncType).html(json.status);
            $("#sync_details_" + sSyncType).html(ptx.ref.sync_details(json));
            // Finish nicely
            ptx.ref.sync_stop(sSyncType, json);
            return;
          default:
            // Default action is to show the status
            $("#sync_progress_" + sSyncType).html(json.status);
            $("#sync_details_" + sSyncType).html(ptx.ref.sync_details(json));
            ptx.ref.oSyncTimer = window.setTimeout(function () { ptx.ref.sync_progress(sSyncType, options); }, 1000);
            break;
        }
      },

      /**
       *  sync_stop
       *      Finalize synchronisation
       *
       */
      sync_stop: function (sSyncType, json) {
        var lHtml = [];

        // Stop the progress calling
        window.clearInterval(ptx.ref.oSyncTimer);
        // Show we are ready
        $("#sync_progress_" + sSyncType).html("Finished synchronizing: " + sSyncType + "<br>" + JSON.stringify(json, null, 2));

      },

      /**
       *  sync_details
       *      Return a string with synchronisation details
       *
       */
      sync_details: function (json) {
        var lHtml = [],
            oCount = {};

        // Validate
        if (json === undefined || !json.hasOwnProperty("count"))
          return "";
        // Get the counts
        oCount = JSON.parse(json['count']);
        // Create a reply
        lHtml.push("<div><table><thead><tr><th></th><th></th></tr></thead><tbody>");
        for (var property in oCount) {
          if (oCount.hasOwnProperty(property)) {
            lHtml.push("<tr><td>" + property + "</td><td>" + oCount[property] + "</td></tr>");
          }
        }
        lHtml.push("</tbody></table></div>");
        // Return as string
        return lHtml.join("\n");
      },
      /**
       * toggle_results
       *   Show or hide the rows belonging to me
       *
       */
      toggle_results: function (elTd, sGroup) {
        var elTable = null,
            elOpen = null;

        try {
          // First get the table start
          elTable = $(elTd).closest("table");
          if (elTable !== null) {
            // Check if there are any visible rows
            elOpen = $(elTable).find(".account-active").not(".hidden").first();
            // Close all rows
            $(elTable).find(".account-pm").addClass("hidden");
            $(elTable).find(".account-active").addClass("hidden");
            if (elOpen.length === 0) {
              // Now show the rows indicated
              $(elTable).find(".account-active." + sGroup).removeClass("hidden");
              // Change the sign to '-'
              $(elTd).html("-");
            } else {
              // Change the sign to "+"
              $(elTd).html("+");
            }
          }

        } catch (ex) {
          private_methods.errMsg("toggle_results", ex);
        }
      },

      /**
       * toggle_textarea_click
       *   Action when user clicks [textarea] element
       *
       */
      toggle_textarea_click: function () {
        var elGroup = null,
            elSpan = null,
            sStatus = "";

        try {
          // Get the following <span> of class td-textarea
          elSpan = $(this).next(".td-textarea");
          // Sanity check
          if (elSpan !== null) {
            // Show it if needed
            if ($(elSpan).hasClass("hidden")) {
              $(elSpan).removeClass("hidden");
            }
            // Hide myself
            $(this).addClass("hidden");
          }
        } catch (ex) {
          private_methods.errMsg("toggle_textarea_click", ex);
        }
      }

    };
  }($, ptx.config));

  return ptx;
}(jQuery, window.ptx || {})); // window.ptx: see http://stackoverflow.com/questions/21507964/jslint-out-of-scope

