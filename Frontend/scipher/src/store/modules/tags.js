import Axios from 'axios';

const state = {
    tags: [],
    tag_search: [],
    popular_tags: [],
    tag_load: true,
    popular_tags_load: true,
};

const getters = {
    TAG: state => id => {
        return state.tags.find(tag => tag.id == id);
    },
};

const mutations = {
    SET_POPULAR_TAGS: (state, payload) => {
        state.popular_tags = payload;
    },
    SEARCH_TAG: (state, payload) => {
        state.tag_search = payload;
    },
    ADD_TAG: (state, payload) => {
        state.tags.push(payload);
    },
};

const actions = {
    async SET_POPULAR_TAGS({ commit, state }) {
        document.body.style.overflow = "hidden";
        state.tags_load = true;
        await Axios
            .get(`/tags/popular?limit=8`)
            .then(function (response) {
                state.tags_load = false;
                commit('SET_POPULAR_TAGS', response.data);
            }).catch(function (error) {
                state.tags_load = false;
                commit('SET_MESSAGE', ["error", `Произошла ошибка загрузки (${error.response ? error.response.status : error})`]);
            })
    },

    ADD_TAG: ({ commit, state }, tag_id) => {
        document.body.style.overflow = "hidden";
        state.tag_load = true;
        Axios
            .get(`/tag/${tag_id}`)
            .then(function (response) {
                commit('ADD_TAG', response.data);
                state.tag_load = false;
                document.body.style.overflow = "scroll"
            }).catch(function (error) {
                commit('SET_MESSAGE', ["error", `Произошла ошибка загрузки (${error.response ? error.response.status : error})`]);
                state.tag_load = false;
                document.body.style.overflow = "scroll"
            })
    },

    SEARCH_TAG: ({ commit }, title) => {
        Axios
            .get(`/tags/${title}/search`)
            .then(function (response) {
                commit('SEARCH_TAG', response.data);
            }).catch(function (error) {
                commit('SET_MESSAGE', ["error", `Произошла ошибка загрузки (${error.response ? error.response.status : error})`])
            })
    },
//!!!
    CREATE_TAG: ({ commit }, data) => {
        Axios
            .post(`/tag`, data)
            .then(function () {
                commit('SET_MESSAGE', []);
            }).catch(function (error) {
                commit('SET_MESSAGE', ["error", `Произошла ошибка загрузки (${error.response ? error.response.status : error})`])
            })
    },
//!!!
};

export default {
    state,
    getters,
    mutations,
    actions,
};