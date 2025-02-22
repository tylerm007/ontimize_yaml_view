import { NgModule } from '@angular/core';
import { RouterModule, Routes } from '@angular/router';
import { MenuGroupHomeComponent } from './home/MenuGroup-home.component';
import { MenuGroupNewComponent } from './new/MenuGroup-new.component';
import { MenuGroupDetailComponent } from './detail/MenuGroup-detail.component';

const routes: Routes = [
  {path: '', component: MenuGroupHomeComponent},
  { path: 'new', component: MenuGroupNewComponent },
  { path: ':id', component: MenuGroupDetailComponent,
    data: {
      oPermission: {
        permissionId: 'MenuGroup-detail-permissions'
      }
    }
  },{
    path: ':menu_group_id/MenuItem', loadChildren: () => import('../MenuItem/MenuItem.module').then(m => m.MenuItemModule),
    data: {
        oPermission: {
            permissionId: 'MenuItem-detail-permissions'
        }
    }
}
];

export const MENUGROUP_MODULE_DECLARATIONS = [
    MenuGroupHomeComponent,
    MenuGroupNewComponent,
    MenuGroupDetailComponent 
];


@NgModule({
  imports: [RouterModule.forChild(routes)],
  exports: [RouterModule]
})
export class MenuGroupRoutingModule { }