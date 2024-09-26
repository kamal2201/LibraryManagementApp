import { createRouter, createWebHashHistory } from 'vue-router'
import HomeView from '../views/HomeView.vue'
import RegisterPage from '../views/RegisterPage.vue'
import LoginPage from '../views/LoginPage.vue'
import AllSections from '../views/AllSections.vue'
import CreateSection from '../views/CreateSection.vue'
import UpdateSection from '../views/UpdateSection.vue';
import AllBooks from '../views/AllBooks.vue'
import CreateBook from '../views/CreateBook.vue'
import UpdateBook from '../views/UpdateBook.vue'
import RequestedBooks from '../views/RequestedBooks.vue';
import ViewSection from '../views/ViewSection.vue'
import MyBooks from '../views/MyBooks.vue'
import AdminStats from '../views/AdminStats.vue'
import SearchPage from '@/views/SearchPage.vue'
import SearchResults from '@/views/SearchResults.vue'

const routes = [
  {
    path: '/',
    name: 'home',
    component: HomeView
  },
  {
    path: '/register',
    name: 'register',
    component: RegisterPage
  },
  {
    path: '/login',
    name: 'login',
    component: LoginPage
  },
  {
    path: '/section',
    name: 'section',
    component: AllSections
  },
  {
    path: '/create_section',
    name: 'create_section',
    component: CreateSection
  },
  {
    path: '/update_section/:id',
    name: 'update_section',
    component: UpdateSection
  },
  {
    path: '/book',
    name: 'book',
    component: AllBooks
  },
  {
    path: '/update_book/:id',
    name: 'update_book',
    component: UpdateBook
  },
  {
    path: '/create_book',
    name: 'create_book',
    component: CreateBook
  },
  {
    path: '/request',
    name: 'request',
    component: RequestedBooks
  },
  {
    path: '/view_section/:sectionId',
    name: 'view_section',
    component: ViewSection
  },
  {
    path: '/my_books',
    name: 'my_books',
    component: MyBooks
  },
  {
    path: '/admin_stats',
    name: 'admin_stats',
    component: AdminStats
  },
  {
    path: '/about',
    name: 'about',
    component: () => import(/* webpackChunkName: "about" */ '../views/AboutView.vue')
  },
  {
    path: '/search',
    name: 'search',
    component: SearchPage
  },
  {
    path: '/search-results',
    name: 'SearchResults',
    component: SearchResults
  }
]

const router = createRouter({
  history: createWebHashHistory(),
  routes
})

export default router
