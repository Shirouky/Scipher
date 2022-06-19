import Vue from 'vue';
import Vuex from 'vuex';
import Axios from 'axios';

import users from './modules/users'
import articles from './modules/articles'
import tags from './modules/tags'
import comments from './modules/comments'
import compilations from './modules/compilations'

Vue.use(Vuex);
Axios.defaults.baseURL = 'http://127.0.0.1:8000'

export const store = new Vuex.Store({
    modules: {
        users,
        articles,
        comments,
        compilations,
        tags
    },
    state: {
        message: {},
        is_auth: false,
        editor_config: {
            toolbar: [
                {
                    name: "document",
                    groups: ["mode", "document", "doctools"],
                    items: [
                        "-",
                        "Save",
                        "NewPage",
                        "ExportPdf",
                        "Preview",
                        "Print",
                        "-",
                        "Templates",
                    ],
                },
                {
                    name: "clipboard",
                    groups: ["clipboard", "undo"],
                    items: ["Cut", "Copy", "Paste", "Undo", "Redo"],
                },
                {
                    name: "editing",
                    groups: ["find", "selection", "spellchecker"],
                    items: ["Find", "Replace", "-", "SelectAll", "-", "Scayt"],
                },
                {
                    name: "forms",
                    items: [
                        "Form",
                        "Checkbox",
                        "Radio",
                        "TextField",
                        "Textarea",
                        "Select",
                        "Button",
                        "ImageButton",
                        "HiddenField",
                    ],
                },
                {
                    name: "basicstyles",
                    groups: ["basicstyles", "cleanup"],
                    items: [
                        "Bold",
                        "Italic",
                        "Underline",
                        "Strike",
                        "Subscript",
                        "Superscript",
                        "-",
                        "CopyFormatting",
                        "RemoveFormat",
                    ],
                },
                {
                    name: "paragraph",
                    groups: ["list", "indent", "blocks", "align", "bidi"],
                    items: [
                        "NumberedList",
                        "BulletedList",
                        "-",
                        "Outdent",
                        "Indent",
                        "-",
                        "Blockquote",
                        "CreateDiv",
                        "-",
                        "JustifyLeft",
                        "JustifyCenter",
                        "JustifyRight",
                        "JustifyBlock",
                        "-",
                        "BidiLtr",
                        "BidiRtl",
                        "Language",
                    ],
                },
                {
                    name: "insert",
                    items: [
                        "Image",
                        "Table",
                        "HorizontalRule",
                        "Smiley",
                        "SpecialChar",
                        "PageBreak",
                        "Iframe",
                    ],
                },
                { name: "styles", items: ["Styles", "Format", "Font", "FontSize"] },
                { name: "colors", items: ["TextColor", "BGColor"] },
                { name: "tools", items: ["Maximize", "ShowBlocks"] },
                { name: "others", items: ["-"] },
            ],
            removePlugins: "elementspath",
            toolbarCanCollapse: true,
            width: "100%",
        },
    },
    getters: {},
    mutations: {
        SET_MESSAGE: (state, payload) => {
            state.message = {
                type: payload[0],
                text: payload[1]
            }
        },
    },
    actions: {}
});