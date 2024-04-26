import { MenuRootItem } from 'ontimize-web-ngx';

import { EntityCardComponent } from './Entity-card/Entity-card.component';

import { EntityAttrCardComponent } from './EntityAttr-card/EntityAttr-card.component';

import { GlobalSettingCardComponent } from './GlobalSetting-card/GlobalSetting-card.component';

import { TabGroupCardComponent } from './TabGroup-card/TabGroup-card.component';

import { TemplateCardComponent } from './Template-card/Template-card.component';


export const MENU_CONFIG: MenuRootItem[] = [
    { id: 'home', name: 'HOME', icon: 'home', route: '/main/home' },
    { id: 'settings', name: 'Settings', icon: 'home', route: '/main/settings'},
    { id: 'data', name: 'DATA', icon: 'remove_red_eye', opened: true,
    items: [
    
        { id: 'Entity', name: 'ENTITY', icon: 'description', route: '/main/Entity' }
    
        ,{ id: 'EntityAttr', name: 'ENTITYATTR', icon: 'description', route: '/main/EntityAttr' }
    
        ,{ id: 'GlobalSetting', name: 'GLOBALSETTING', icon: 'description', route: '/main/GlobalSetting' }
    
        ,{ id: 'TabGroup', name: 'TABGROUP', icon: 'description', route: '/main/TabGroup' }
    
        ,{ id: 'Template', name: 'TEMPLATE', icon: 'description', route: '/main/Template' }
    
    ] 
    }
    ,{ id: 'about', name: 'About', icon: 'home', route: '/main/about'}
    ,{ id: 'logout', name: 'LOGOUT', route: '/login', icon: 'power_settings_new', confirm: 'yes' }
];

export const MENU_COMPONENTS = [

    EntityCardComponent

    ,EntityAttrCardComponent

    ,GlobalSettingCardComponent

    ,TabGroupCardComponent

    ,TemplateCardComponent

];