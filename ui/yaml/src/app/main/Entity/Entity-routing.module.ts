import { NgModule } from '@angular/core';
import { RouterModule, Routes } from '@angular/router';
import { EntityHomeComponent } from './home/Entity-home.component';
import { EntityNewComponent } from './new/Entity-new.component';
import { EntityDetailComponent } from './detail/Entity-detail.component';

const routes: Routes = [
  {path: '', component: EntityHomeComponent},
  { path: 'new', component: EntityNewComponent },
  { path: ':name', component: EntityDetailComponent,
    data: {
      oPermission: {
        permissionId: 'Entity-detail-permissions'
      }
    }
  }
];

export const ENTITY_MODULE_DECLARATIONS = [
    EntityHomeComponent,
    EntityNewComponent,
    EntityDetailComponent 
];


@NgModule({
  imports: [RouterModule.forChild(routes)],
  exports: [RouterModule]
})
export class EntityRoutingModule { }