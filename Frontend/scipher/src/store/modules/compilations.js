import Axios from 'axios';

const state = {
    user_compilations: [[]],
    compilations: [],
    compilations_load: true,
};

const getters = {

};

const mutations = {
    SET_USER_COMPILATIONS: (state, payload) => {
        state.user_compilations = payload;
    },
    SET_COMPILATIONS: (state, payload) => {
        state.compilations = payload;
    },
};

const actions = {
    SET_USER_COMPILATIONS: ({ commit }) => {
        Axios
            .get(`/compilations/user`)
            .then(function (response) {
                if (response.data.length == 0) {
                    commit('SET_USER_COMPILATIONS', [[]]);
                } else {
                    commit('SET_USER_COMPILATIONS', response.data);
                }
            }).catch(function (error) {
                commit('SET_MESSAGE', ["error", `Произошла ошибка загрузки (${error.response ? error.response.status : error})`]);
            })
    },

    SET_COMPILATIONS: ({ commit, state }, article_id) => {
        Axios
            .get(`/compilations/article/${article_id}`)
            .then(function (response) {
                state.compilations_load = false;
                commit('SET_COMPILATIONS', response.data);
            }).catch(function (error) {
                state.compilations_load = false;
                commit('SET_MESSAGE', ["error", `Произошла ошибка загрузки (${error.response ? error.response.status : error})`]);
            })
    },
    
    SAVE_COMPILATION: ({ commit }, data) => {
        Axios
            .patch(`/compilation/${data.compilation_id}/article/${data.article_id}`, data)
            .then(function (response) {
                commit('ADD_COMMENTS', response.data);
            }).catch(function (error) {
                commit('SET_MESSAGE', ["error", `Произошла ошибка загрузки (${error.response ? error.response.status : error})`])
            })
    },

    CREATE_COMPILATION: ({ commit }, data) => {
        Axios
            .post(`/compilation`, data)
            .then(function (response) {
                commit('ADD_COMPILATION', response.data);
            }).catch(function (error) {
                commit('SET_MESSAGE', ["error", `Произошла ошибка загрузки (${error.response ? error.response.status : error})`]);
            })
    },
};

export default {
    state,
    getters,
    mutations,
    actions,
};