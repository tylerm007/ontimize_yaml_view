import { Config } from 'ontimize-web-ngx';

import { MENU_CONFIG } from './shared/app.menu.config';
import { SERVICE_CONFIG } from './shared/app.services.config';
import { environment } from 'src/environments/environment';

export const CONFIG: Config = {
  //apiEndpoint: environment.apiEndpoint,
  apiEndpoint:  (window['__env'] !== undefined) ? window['__env']['apiUrl'] : environment.apiEndpoint,

  //production: environment.production,
  bundle: {
    path: 'bundle'
  },
  // Application identifier. Is the unique package identifier of the app.
  // It is used when storing or managing temporal data related with the app.
  // By default is set as 'ontimize-web-uuid'.
  uuid: 'com.ontimize.web.ngx.jee.seed15x',

  // Title of the app
  title: 'ApiLogicServer Yaml Editor',

  //  Language of the application.
  locale: 'en',

  // The service type used (Ontimize REST standard, Ontimize REST JEE
  // or custom implementation) in the whole application. JSONAPI is also supported.
  serviceType: 'OntimizeEE',

  // Configuration parameters of application services.
  servicesConfiguration: SERVICE_CONFIG,

  appMenuConfiguration: MENU_CONFIG,

  applicationLocales: ['en', 'es', 'fr'], // 'de', 'it', 'pt', 'zh', 'ja', 'ko'],

  exportConfiguration: {
    path: '/export'
  }

  
  //,startSessionPath: '/auth/login',
  

};
