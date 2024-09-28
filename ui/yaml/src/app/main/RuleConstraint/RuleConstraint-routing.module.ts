import { NgModule } from '@angular/core';
import { RouterModule, Routes } from '@angular/router';
import { RuleConstraintHomeComponent } from './home/RuleConstraint-home.component';
import { RuleConstraintNewComponent } from './new/RuleConstraint-new.component';
import { RuleConstraintDetailComponent } from './detail/RuleConstraint-detail.component';

const routes: Routes = [
  {path: '', component: RuleConstraintHomeComponent},
  { path: 'new', component: RuleConstraintNewComponent },
  { path: ':id', component: RuleConstraintDetailComponent,
    data: {
      oPermission: {
        permissionId: 'RuleConstraint-detail-permissions'
      }
    }
  }
];

export const RULECONSTRAINT_MODULE_DECLARATIONS = [
    RuleConstraintHomeComponent,
    RuleConstraintNewComponent,
    RuleConstraintDetailComponent 
];


@NgModule({
  imports: [RouterModule.forChild(routes)],
  exports: [RouterModule]
})
export class RuleConstraintRoutingModule { }