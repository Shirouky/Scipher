import Axios from 'axios';
import VueCookies from 'vue-cookies'

const state = {
  user: {},
  best_users_load: true,
  user_load: true,
  user_search_load: true,
  code: 0,
  enable_email: false,
  user_search: [],
  users: [{}],
  best_users: [],
};

const getters = {
  USER: state => id => {
    return state.users.find(user => user.id == id);
  },
};

const mutations = {
  SET_USER: (state, payload) => {
    state.user = payload;
    VueCookies.set("id", state.user.id);
  },
  SET_TOKEN: (rootState, payload) => {
    rootState.token = payload.access_token
    VueCookies.set("token", payload.access_token)
    Axios.defaults.headers.common['Authorization'] = `Bearer ${payload.access_token}`;
  },
  TOKEN: (rootState) => {
    const token = VueCookies.get("token");
    if (token) {
      rootState.is_auth = true
      Axios.defaults.headers.common['Authorization'] = `Bearer ${token}}`;
    }
  },
  SET_BEST_USERS: (state, payload) => {
    state.best_users = payload;
  },
  SET_CONFIRMATION: (state, payload) => {
    state.code = payload;
    state.enable_email = true;
  },
  ADD_USER: (state, payload) => {
    state.users.push(payload);
  },
  SEARCH_USER: (state, payload) => {
    state.user_search = payload;
  },
};

const actions = {
  async SET_BEST_USERS({ commit, state }) {
    document.body.style.overflow = "hidden";
    state.best_users_load = true;
    await Axios
      .get(`/users/best?limit=10`)
      .then(function (response) {
        state.best_users_load = false;
        commit('SET_BEST_USERS', response.data);
      }).catch(function (error) {
        state.best_users_load = false;
        commit('SET_MESSAGE', ["error", `Произошла ошибка загрузки (${error.response ? error.response.status : error})`]);
      })
  },

  SET_USER: ({ commit }) => {
    Axios
      .get(`/user`)
      .then(function (response) {
        commit('SET_USER', response.data);
      }).catch(function (error) {
        commit('SET_MESSAGE', ["error", `Произошла ошибка загрузки (${error.response ? error.response.status : error})`]);
      })
  },

  ADD_USER: ({ commit }, user_id) => {
    Axios
      .get(`/user/${user_id}`)
      .then(function (response) {
        commit('ADD_USER', response.data);
      }).catch(function (error) {
        commit('SET_MESSAGE', ["error", `Произошла ошибка загрузки (${error.response ? error.response.status : error})`]);
      })
  },

  SEND_CONFIRMATION: ({ commit }, email) => {
    Axios
      .get(`/user/${email}/email`)
      .then(function (response) {
        const code = response.data;
        if (code) {
          commit('SET_MESSAGE', ["message", "Письмо подтверждения было отправлено на почту"])
          commit('SET_CONFIRMATION', code)
        }
        else commit('SET_MESSAGE', ["error", "Пользователь с таким email уже зарегистрирован на сайте"])
      }).catch(function (error) {
        commit('SET_MESSAGE', ["error", `Произошла ошибка загрузки (${error.response ? error.response.status : error})`])
      })
  },


  SEARCH_USER: ({ commit }, username) => {
    Axios
      .get(`/users/${username}/search`)
      .then(function (response) {
        commit('SEARCH_USER', response.data);
      }).catch(function (error) {
        commit('SET_MESSAGE', ["error", `Произошла ошибка загрузки (${error.response ? error.response.status : error})`]);
      })
  },

  SAVE_USER: ({ commit }, data) => {
    Axios
      .patch(`/user/edit`, data)
      .then(function () {
        commit('SET_MESSAGE', ["message", "Изменения успешно сохранены!"]);
      }).catch(function (error) {
        commit('SET_MESSAGE', ["error", `Произошла ошибка загрузки (${error.response ? error.response.status : error})`])
      })
  },
  //!!!
  DELETE_USER: ({ commit }) => {
    Axios
      .patch(`/user/delete`)
      .catch(function (error) {
        commit('SET_MESSAGE', ["error", `Произошла ошибка загрузки (${error.response ? error.response.status : error})`])
      })
  },
  //!!!

  LOGIN_USER: async ({ commit }, data) => {
    var dat = new FormData()
    dat.append('username', data.email)
    dat.append('password', data.password)
    Axios
      .post(`/user/token`, dat, {
        headers: {
          "Content-Type": "application/x-www-form-urlencoded",
        }
      })
      .then(function (response) {
        commit('SET_TOKEN', response.data)
        commit('SET_USER', response.data);
      }).catch(function (error) {
        commit('SET_MESSAGE', ["error", `Произошла ошибка загрузки (${error.response ? error.response.status : error})`]);
      })

  },

  LOGOUT_USER({ commit }) {
    commit('SET_USER', {});
    VueCookies.remove("id");
    VueCookies.remove("token");
    Axios
      .post(`/user/logout`)
      .catch(function (error) {
        commit('SET_MESSAGE', ["error", `Произошла ошибка загрузки (${error.response ? error.response.status : error})`]);
      })
  },

  REGISTER_USER: ({ commit }, data) => {
    Axios
      .post(`/user`, data)
      .then(function (response) {
        commit('SET_MESSAGE', ["message", "Регистрация прошла успешно!"]);
        commit('SET_USER', response.data);
      }).catch(function (error) {
        commit('SET_MESSAGE', ["error", `Произошла ошибка загрузки (${error.response ? error.response.status : error})`]);
      })
  },


  SAVE_AVATAR: ({ commit }, file) => {
    var data = new FormData()
    data.append('file', file)
    Axios
      .post(`/user/avatar`, data, { headers: { "Content-Type": "multipart/form-data; " } })
      .catch(function (error) {
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