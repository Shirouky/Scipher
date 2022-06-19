import Axios from 'axios';
import Vue from 'vue';
import router from '../../router'

const state = {
    latest_articles: [],
    popular_articles: [],
    user_viewed: [],
    user_read: [],
    authorship_published: [],
    authorship_all: [],
    authorship_in_work: [],
    tag_articles: [],
    article_search: [],
    article_load: true,
    latest_articles_load: true,
    popular_articles_load: true,
    articles: [{}],
};

const getters = {
    ARTICLE: state => id => {
        return state.articles.find(article => article.id == id);
    },
};

const mutations = {
    SET_USER_VIEWED: (state, payload) => {
        state.user_viewed = payload;
    },
    SET_USER_READ: (state, payload) => {
        state.user_read = payload;
    },
    SET_LATEST_ARTICLES: (state, payload) => {
        state.latest_articles = payload;
    },
    SET_POPULAR_ARTICLES: (state, payload) => {
        state.popular_articles = payload;
    },
    SET_USER_AUTHORSHIP: (state, payload) => {
        state.authorship_all = payload;
        state.authorship_published = [];
        state.authorship_in_work = [];
        payload.forEach(elem => {
            if (elem.published) state.authorship_published.push(elem)
            else state.authorship_in_work.push(elem)
        });
    },
    SET_COMMENTS: (state, payload) => {
        var article = state.articles.findIndex(article => article.id == payload.article_id) + 1;
        state.articles[article].comments = payload;
    },
    ADD_COMMENTS: (state, payload) => {
        var article = state.articles.findIndex(article => article.id == payload.article_id) + 1;
        var article_copy = state.articles[article];
        article_copy.comments = article_copy.comments.concat(payload);
        Vue.set(state.articles, article, article_copy);
    },
    ADD_ARTICLE: (state, payload) => {
        payload.comments = []
        state.articles.push(payload);
    },
    SET_TAG_ARTICLES: (state, payload) => {
        state.tag_articles = payload;
    },
    SET_ARTICLE: (state, payload) => {
        var article = state.articles.findIndex(article => article.id == payload.id) + 1;
        Vue.set(state.articles, article, payload);
    },
    SEARCH_ARTICLE: (state, payload) => {
        state.article_search = payload;
    },
};

const actions = {
    ADD_ARTICLE: ({ commit, state, dispatch }, article_id) => {
        document.body.style.overflow = "hidden";
        state.article_load = true;
        Axios
            .get(`/article/${article_id}`)
            .then(function (response) {
                commit('ADD_ARTICLE', response.data);
                dispatch('SET_ARTICLE_COMMENTS', article_id)
                state.article_load = false;
                document.body.style.overflow = "scroll"
            }).catch(function (error) {
                state.article_load = false;
                document.body.style.overflow = "scroll"
                commit('SET_MESSAGE', ["error", `Произошла ошибка загрузки (${error.response ? error.response.status : error})`])
            })
    },

    async SET_LATEST_ARTICLES({ commit, state }) {
        document.body.style.overflow = "hidden";
        state.latest_articles_load = true;
        await Axios
            .get(`/articles/last?limit=10`)
            .then(function (response) {
                state.latest_articles_load = false;
                commit('SET_LATEST_ARTICLES', response.data);
            }).catch(function (error) {
                state.latest_articles_load = false;
                commit('SET_MESSAGE', ["error", `Произошла ошибка загрузки (${error.response ? error.response.status : error})`]);
            })
    },

    async SET_POPULAR_ARTICLES({ commit, state }) {
        document.body.style.overflow = "hidden";
        state.popular_articles_load = true;
        await Axios
            .get(`/articles/popular?limit=10`)
            .then(function (response) {
                state.popular_articles_load = false;
                commit('SET_POPULAR_ARTICLES', response.data);
            }).catch(function (error) {
                state.popular_articles_load = false;
                commit('SET_MESSAGE', ["error", `Произошла ошибка загрузки (${error.response ? error.response.status : error})`]);
                commit('SET_POPULAR_ARTICLES', []);
            })
    },

    SET_USER_AUTHORSHIP: ({ commit }, uid) => {
        Axios
            .get(`/articles/${uid}/authorship`)
            .then(function (response) {
                commit('SET_USER_AUTHORSHIP', response.data);
            }).catch(function (error) {
                commit('SET_MESSAGE', ["error", `Произошла ошибка загрузки (${error.response ? error.response.status : error})`]);
            })
    },

    SET_TAG_ARTICLES: ({ commit }, tag_id) => {
        Axios
            .get(`/articles/${tag_id}/tag`)
            .then(function (response) {
                commit('SET_TAG_ARTICLES', response.data);
            }).catch(function (error) {
                commit('SET_MESSAGE', ["error", `Произошла ошибка загрузки (${error.response ? error.response.status : error})`]);
            })
    },

    SET_USER_READ: ({ commit, rootState }) => {
        if (rootState.is_auth) {
            Axios
                .get(`/articles/read`)
                .then(function (response) {
                    commit('SET_USER_READ', response.data);
                }).catch(function (error) {
                    commit('SET_MESSAGE', ["error", `Произошла ошибка загрузки (${error.response ? error.response.status : error})`]);
                })
        }
    },

    SET_USER_VIEWED: ({ commit, rootState }) => {
        if (rootState.is_auth) {
            Axios
                .get(`/articles/view`)
                .then(function (response) {
                    commit('SET_USER_VIEWED', response.data);
                }).catch(function (error) {
                    commit('SET_MESSAGE', ["error", `Произошла ошибка загрузки (${error.response ? error.response.status : error})`]);
                })
        }
    },

    SAVE_ARTICLE: ({ commit, rootState }, data) => {
        if (rootState.is_auth) {
            Axios
                .patch(`/articles/${data.article_id}/edit`, data.data)
                .then(function () {
                    commit('SET_MESSAGE', ["message", "Статья успешно сохранена!"]);
                }).catch(function (error) {
                    commit('SET_MESSAGE', ["error", `Произошла ошибка загрузки (${error.response ? error.response.status : error})`])
                })
        }
    },

    PUBLISH_ARTICLE: ({ commit, rootState }, article_id) => {
        if (rootState.is_auth) {
            Axios
                .patch(`/article/${article_id}/publish`, { "is_publish": true })
                .catch(function (error) {
                    commit('SET_MESSAGE', ["error", `Произошла ошибка загрузки (${error.response ? error.response.status : error})`])
                })
        }
    },

    SET_READ: ({ commit, rootState }, article_id) => {
        if (rootState.is_auth) {
            Axios
                .patch(`/article/${article_id}/read`)
                .catch(function (error) {
                    commit('SET_MESSAGE', ["error", `Произошла ошибка загрузки (${error.response ? error.response.status : error})`]);
                })
        }
    },

    ADD_VIEWED: ({ commit, rootState }, article_id) => {
        if (rootState.is_auth) {
            Axios
                .patch(`/article/${article_id}/view`)
                .catch(function (error) {
                    commit('SET_MESSAGE', ["error", `Произошла ошибка загрузки (${error.response ? error.response.status : error})`]);
                })
        }
    },

    DELETE_ARTICLE: ({ commit }, article_id) => {
        Axios
            .patch(`/article/${article_id}/delete`)
            .then(function () {
                commit("SET_ARTICLE", [])
            }).catch(function (error) {
                commit('SET_MESSAGE', ["error", `Произошла ошибка загрузки (${error.response ? error.response.status : error})`])
            })
    },
    //!!!
    SAVE_RATING: ({ commit }, data) => {
        Axios
            .patch(`/article/${data.article_id}/rating/${data.rating}`)
            .catch(function (error) {
                commit('SET_MESSAGE', ["error", `Произошла ошибка загрузки (${error.response ? error.response.status : error})`]);
            })
    },
    //!!!
    SAVE_ARTICLE_BACK: ({ commit }, data) => {
        var dat = new FormData()
        dat.append('file', data.file)
        Axios
            .post(`/img/article/${data.article_id}/back`, dat, { headers: { "Content-Type": "multipart/form-data; " } })
            .catch(function (error) {
                commit('SET_MESSAGE', ["error", `Произошла ошибка загрузки (${error.response ? error.response.status : error})`])
            })
    },

    CREATE_ARTICLE: ({ commit }, title) => {
        Axios
            .post(`/article/${title}`)
            .then(function (response) {
                router.push("/article/edit/" + response.data)
            }).catch(function (error) {
                commit('SET_MESSAGE', ["error", `Произошла ошибка загрузки (${error.response ? error.response.status : error})`]);
            })
    },
    SEARCH_ARTICLE: ({ commit }, data) => {
        Axios
            .post(`search`, data)
            .then(function (response) {
                commit('SEARCH_ARTICLE', response.data);
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