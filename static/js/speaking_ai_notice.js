/**
 * Gate the first speaking record action behind the one-time AI notice.
 * Call with CSS selectors for buttons that start a recording.
 */
(function (global) {
  function gateSpeakingRecord(selectors) {
    if (!global.__bsSpeakingNoticePending) return;
    var list = Array.isArray(selectors) ? selectors : [selectors];
    list.forEach(function (sel) {
      document.querySelectorAll(sel).forEach(function (el) {
        el.addEventListener(
          "click",
          function (e) {
            if (!global.__bsSpeakingNoticePending) return;
            e.preventDefault();
            e.stopImmediatePropagation();
            var notice = document.getElementById("bs-speak-notice");
            if (notice) notice.hidden = false;
          },
          true
        );
      });
    });
  }
  global.bsGateSpeakingRecord = gateSpeakingRecord;
})(window);
