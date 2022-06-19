import Vue from 'vue'
import VueCookies from 'vue-cookies'
import VueRouter from 'vue-router'
import HomeView from '../views/HomeView.vue'
import SearchArticleView from '../views/SearchArticleView.vue'
import SearchUserView from '../views/SearchUserView.vue'
import ArticleView from '../views/ArticleView.vue'
import ArticleEditView from '../views/ArticleEditView.vue'
import TagView from '../views/TagView.vue'
import UserProfile from '../views/UserProfileView.vue'
import UserProfileEdit from '../views/UserProfileEditView.vue'
import NotFound from '../views/NotFoundView.vue'
import RegisterView from '../views/RegisterView.vue'

Vue.use(VueRouter)

const routes = [
  {
    path: '/',
    name: 'home',
    component: HomeView,
  },
  {
    path: '/search/article',
    name: 'searchArticle',
    props: true,
    component: SearchArticleView,
  },
  {
    path: '/search/user',
    name: 'searchUser',
    props: true,
    component: SearchUserView,
  },
  {
    path: '/article/:id',
    name: 'article',
    component: ArticleView,
  },
  {
    path: '/article/edit/:id',
    name: 'articleEdit',
    component: ArticleEditView,
  },
  {
    path: '/user/:id',
    name: 'userProfile',
    component: UserProfile,
  },
  {
    path: '/user/edit/:id',
    name: 'userProfileEdit',
    component: UserProfileEdit,
    beforeEnter: (to, from, next) => {
      if (VueCookies.get("id") == to.params.id) {
        next()
      } else {
        next('/')
      }
    }
  },
  {
    path: '/register',
    name: 'register',
    component: RegisterView,
  },
  {
    path: '/tag/:id',
    name: 'tag',
    component: TagView,
  },
  {
    path: "*",
    component: NotFound,
  },
]

const router = new VueRouter({
  mode: 'history',
  base: process.env.BASE_URL,
  routes
})

export default router
