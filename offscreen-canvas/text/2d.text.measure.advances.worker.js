// DO NOT EDIT! This test has been generated by tools/gentest.py.
// OffscreenCanvas test in a worker:2d.text.measure.advances
// Description:Testing width advances for OffscreenCanvas
// Note:

importScripts("/resources/testharness.js");
importScripts("/common/canvas-tests.js");

var t = async_test("Testing width advances for OffscreenCanvas");
t.step(function() {

var offscreenCanvas = new OffscreenCanvas(100, 50);
var ctx = offscreenCanvas.getContext('2d');

deferTest();
var f = new FontFace("CanvasTest", "/fonts/CanvasTest.ttf");
let fonts = (document ? document.fonts : self.fonts);
fonts.add(f);
fonts.ready.then(() => {
    step_timeout(t.step_func_done(function () {
        ctx.font = '50px CanvasTest';
        ctx.direction = 'ltr';
        ctx.align = 'left'
        // Some platforms may return '-0'.
        _assertSame(Math.abs(ctx.measureText('Hello').advances[0]), 0, "Math.abs(ctx.measureText('Hello').advances[\""+(0)+"\"])", "0");
        // Different platforms may render text slightly different.
        _assert(ctx.measureText('Hello').advances[1] >= 36, "ctx.measureText('Hello').advances[\""+(1)+"\"] >= 36");
        _assert(ctx.measureText('Hello').advances[2] >= 58, "ctx.measureText('Hello').advances[\""+(2)+"\"] >= 58");
        _assert(ctx.measureText('Hello').advances[3] >= 70, "ctx.measureText('Hello').advances[\""+(3)+"\"] >= 70");
        _assert(ctx.measureText('Hello').advances[4] >= 80, "ctx.measureText('Hello').advances[\""+(4)+"\"] >= 80");

        var tm = ctx.measureText('Hello');
        _assertSame(ctx.measureText('Hello').advances[0], tm.advances[0], "ctx.measureText('Hello').advances[\""+(0)+"\"]", "tm.advances[\""+(0)+"\"]");
        _assertSame(ctx.measureText('Hello').advances[1], tm.advances[1], "ctx.measureText('Hello').advances[\""+(1)+"\"]", "tm.advances[\""+(1)+"\"]");
        _assertSame(ctx.measureText('Hello').advances[2], tm.advances[2], "ctx.measureText('Hello').advances[\""+(2)+"\"]", "tm.advances[\""+(2)+"\"]");
        _assertSame(ctx.measureText('Hello').advances[3], tm.advances[3], "ctx.measureText('Hello').advances[\""+(3)+"\"]", "tm.advances[\""+(3)+"\"]");
        _assertSame(ctx.measureText('Hello').advances[4], tm.advances[4], "ctx.measureText('Hello').advances[\""+(4)+"\"]", "tm.advances[\""+(4)+"\"]");
    }), 500);
});

t.done();

});
done();
