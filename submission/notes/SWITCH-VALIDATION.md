# Switch feature and template validation

Docs were consulted through the switch-docs MCP before implementation. No new
project dependencies were installed. Source example inspected locally:
`examples/agent-templates/triage-pair.template.yaml`, upstream checkout a9dea37150970dd9200fbdfabea8ee1761211203.

| Confirmed feature | Source |
| --- | --- |
| Templates create agents before room; params, kickoff, Console import/use | [Template guide](https://docs.switchagents.ai/switch-rooms/administer/room-templates) |
| v1 keys, typed provider/location/directory/bridge/user params, inline instructions, addressing, room docs | [Template language](https://github.com/sandbox-quantum/switch/blob/main/docs/TEMPLATES.md), [triage-pair](https://github.com/sandbox-quantum/switch/blob/main/examples/agent-templates/triage-pair.template.yaml) |
| Shared instructions, agent-created room documents, author-only document updates | [Payments room](https://docs.switchagents.ai/switch-rooms/building/payments-room) |
| Room documents/shared context available across room agents | [Shared context](https://docs.switchagents.ai/switch-rooms/using/shared-context) |
| `post_message`, addressed handoffs, `read_context`, create/update room document operations | [Agent protocol](https://docs.switchagents.ai/switch-rooms/internals/agent-protocol) |
| Actual message sender/name/id; opaque participant IDs | [Agent events](https://docs.switchagents.ai/switch-rooms/internals/agent-events) |
| Anyone addressing includes fellow room members | [Agent settings](https://docs.switchagents.ai/switch-rooms/getting-started/agent-settings#choose-who-can-instruct-the-agent) |

## Workflow design

Switch's shared room context and document tools keep scope, policy and progress
visible to teammates and agents. Direct human messages supply the sign-off record;
the coordinator captures each actual author and reference before invoking the
receipt-bound release gate. When requirements change, the sender updates the draft
state and posts a visible retraction notice.

## Integration boundaries and extension points

This implementation uses shared room documents for its scope, policy and task
records. The coordinator passes the observed chat author and message reference into
the local receipt ledger; the gate is a trusted-workstation control, and its SQLite
ledger is not tamper-resistant. A stale draft is marked retracted and a new notice
is posted—the earlier chat message remains visible. Teams can extend this pattern
with authenticated identity, protected audit storage and their existing delivery
transport.

## Validation performed

The Switch Console runtime validated the parameterized team template.
`lint_template` returned
`errors: []`, `warnings: []`; `template_kind` returned `group`; `agent_slots` returned
three roles, each with provider/location/shared-directory parameters. The room half
was resolved with isolated validation inputs and parsed with
`RoomYamlService.parse_template`: RoomSpec, three agents, creator plus requester
and approver, one signoff-rule document, and resolved coordinator kickoff. The
completed live Discord workflow is shown in the [demo](../promise-keeper-live-demo.mp4).

To repeat on this Mac from the project root (no installs):

```sh
PYTHONPATH='/Applications/Switch Console.app/Contents/Resources/local-server/switch/site-packages:/Applications/Switch Console.app/Contents/Resources/local-server/switch/src/core' '/Applications/Switch Console.app/Contents/Resources/local-server/python/bin/python3' - <<'PYCODE'
from pathlib import Path
from dataclasses import asdict
from switch_core.template_lint import lint_template
from switch_core.agent_templates import agent_slots, room_document, template_kind
from switch_core.rooms_yaml import RoomYamlService
text = Path('switch-room.template.yaml').read_text()
print(asdict(lint_template(text)))
print(template_kind(text), [slot.name for slot in agent_slots(text)])
inputs = dict(team='validation', requester='sam-validation', approver='priya-validation', bridge='Validation bridge', directory='/tmp/validation-only', provider='codex', location='local')
filled = {'{team}-'+role: 'validation-'+role for role in ['coordinator','builder','sender']}
room, values = room_document(text, filled, inputs)
parsed = object.__new__(RoomYamlService).parse_template(room, values, builtins={'$creator':'validation-creator'})
print(type(parsed.spec).__name__, parsed.spec.agents, parsed.spec.users)
print([doc.name for doc in parsed.spec.docs], parsed.kickoff)
PYCODE
```

For a new team, connect the bridge in Console, make sure the machine is
online/provider signed in and agent management enabled, then **Templates → Import
template → paste YAML → save → Use template**. Select unique prefix, bridge, real
human usernames and SAME absolute prepared directory for all agents. Review three
agent cards, select **Create all** and check actual results: three ready agents,
room membership, signoff-rule and kickoff. Then follow [DEMO.md](../../DEMO.md) with
a requester and an independent reviewer to see the complete workflow in your chat.
