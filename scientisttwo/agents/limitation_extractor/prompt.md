Extract the core limitations of the method in this task.

<task_title>
{{task_title}}
</task_title>

<paper>
{{paper}}
</paper>

<code_overview>
{{code_overview}}
</code_overview>

<rules>
{{rules}}
</rules>

<current_limitations>
{{current_limitations}}
</current_limitations>

<feedback>
{{feedback}}
</feedback>

If `current_limitations` is empty (blank, `[]` or `none`), this is the first call: extract the set
from scratch. Otherwise return the full set: every earlier limitation under its id, corrected where
the feedback shows it is wrong, plus each missing limitation the feedback names, under a new id.
Return the structured output only.
