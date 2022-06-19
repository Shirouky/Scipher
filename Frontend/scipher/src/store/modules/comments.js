import Axios from 'axios';

const state = {
    user_comments: [],
};

const getters = {

};

const mutations = {
    SET_USER_COMMENTS: (state, payload) => {
        state.user_comments = payload;
    },
};

const actions = {
    SET_ARTICLE_COMMENTS: ({ commit }, article_id) => {
        Axios
            .get(`/comments/${article_id}/article`)
            .then(function (response) {
                commit('SET_USER_COMMENTS', response.data);
            }).catch(function (error) {
                commit('SET_MESSAGE', ["error", `Произошла ошибка загрузки (${error.response ? error.response.status : error})`]);
            })
    },
//!!!
    SET_COMMENTS_LIKE: ({ commit }) => {
        Axios
            .get(`/comments/like`)
            .then(function (response) {
                commit('SET_USER_COMMENTS', response.data);
            }).catch(function (error) {
                commit('SET_MESSAGE', ["error", `Произошла ошибка загрузки (${error.response ? error.response.status : error})`]);
            })
    },
//!!!
    SET_USER_COMMENTS: ({ commit }) => {
        Axios
            .get(`/comments/user`)
            .then(function (response) {
                commit('SET_USER_COMMENTS', response.data);
            }).catch(function (error) {
                commit('SET_MESSAGE', ["error", `Произошла ошибка загрузки (${error.response ? error.response.status : error})`]);
            })
    },

    SET_LIKES: ({ commit }, comment_id) => {
        Axios
            .patch(`/comment/${comment_id}/like`)
            .catch(function (error) {
                commit('SET_MESSAGE', ["error", `Произошла ошибка загрузки (${error.response ? error.response.status : error})`]);
            })
    },
//!!!
    UPDATE_COMMENT_TEXT: ({ commit }, data) => {
        Axios
            .patch(`/comment/${data.comment_id}/text/${data.text}`)
            .catch(function (error) {
                commit('SET_MESSAGE', ["error", `Произошла ошибка загрузки (${error.response ? error.response.status : error})`]);
            })
    },
//!!!
    SEND_COMMENT: ({ commit }, data) => {
        Axios
            .post(`/comment`, data)
            .then(function (response) {
                commit('ADD_COMMENTS', response.data);
            }).catch(function (error) {
                commit('SET_MESSAGE', ["error", `Произошла ошибка загрузки (${error.response ? error.response.status : error})`])
            })
    },
};

export default {
    state,
    getters,
    mutations,
    actions,
};