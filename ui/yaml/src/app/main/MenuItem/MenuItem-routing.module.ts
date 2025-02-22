import { NgModule } from '@angular/core';
import { RouterModule, Routes } from '@angular/router';
import { MenuItemHomeComponent } from './home/MenuItem-home.component';
import { MenuItemNewComponent } from './new/MenuItem-new.component';
import { MenuItemDetailComponent } from './detail/MenuItem-detail.component';

const routes: Routes = [
  {path: '', component: MenuItemHomeComponent},
  { path: 'new', component: MenuItemNewComponent },
  { path: ':id', component: MenuItemDetailComponent,
    data: {
      oPermission: {
        permissionId: 'MenuItem-detail-permissions'
      }
    }
  },{
    path: ':menu_item_id/Page', loadChildren: () => import('../Page/Page.module').then(m => m.PageModule),
    data: {
        oPermission: {
            permissionId: 'Page-detail-permissions'
        }
    }
}
];

export const MENUITEM_MODULE_DECLARATIONS = [
    MenuItemHomeComponent,
    MenuItemNewComponent,
    MenuItemDetailComponent 
];


@NgModule({
  imports: [RouterModule.forChild(routes)],
  exports: [RouterModule]
})
export class MenuItemRoutingModule { }