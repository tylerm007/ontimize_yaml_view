import {CUSTOM_ELEMENTS_SCHEMA, NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';
import { OntimizeWebModule } from 'ontimize-web-ngx';
import { SharedModule } from '../../shared/shared.module';
import  {MENUITEM_MODULE_DECLARATIONS, MenuItemRoutingModule} from  './MenuItem-routing.module';

@NgModule({

  imports: [
    SharedModule,
    CommonModule,
    OntimizeWebModule,
    MenuItemRoutingModule
  ],
  declarations: MENUITEM_MODULE_DECLARATIONS,
  exports: MENUITEM_MODULE_DECLARATIONS,
  schemas: [CUSTOM_ELEMENTS_SCHEMA]
})
export class MenuItemModule { }