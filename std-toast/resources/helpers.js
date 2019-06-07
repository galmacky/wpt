import { showToast } from 'std:toast';

// helper functions to keep tests from bleeding into each other

const runTest = (testFn, name, toast) => {
    try {
        test(() => {
            testFn(toast);
        }, name);
    } finally {
        toast.remove();
    }
};

export const testToastElement = (testFn, name) => {
    document.querySelector('main').innerHTML = `<std-toast id="test">Message</std-toast>`;
    const toast = document.querySelector('#test');

    runTest(testFn, name, toast);
};

export const testShowToast = (testFn, name) => {
    const toast = showToast("message");

    runTest(testFn, name, toast);
};

export const assertToastShown = (toast) => {
    assert_not_equals(window.getComputedStyle(toast).display, 'none');
    assert_true(toast.hasAttribute('open'));
};

export const assertToastNotShown = (toast) => {
    assert_equals(window.getComputedStyle(toast).display, 'none');
    assert_false(toast.hasAttribute('open'));
};

export class EventCounter {
    count = 0;

    getCallback() {
        return () => {this.count++};
    }

    getCount() {
        return this.count;
    }
}
