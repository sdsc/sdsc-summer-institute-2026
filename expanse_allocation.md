# Expanse Allocation for SI26

## Account

| Field | Value |
|-------|-------|
| Slurm account | `sdp173` |
| ACCESS project | CIS261077 |
| TG project | TG-CIS261077 |
| Total allocation | 89,546 core-hours |
| Total spent | 289 core-hours |
| Expiration | June 2, 2027 |
| PI | zonca |

## Reservations

| Name | Partition | Nodes | Cores | QOS | Users |
|------|-----------|-------|-------|-----|-------|
| si26cpu | compute | 52 | 6,656 | normal-eot | mkandes |
| si26gpu | gpu | 13 | 520 | gpu-shared-eot | mkandes |

**Note:** Reservations are restricted to `Users=mkandes`. zonca and participants cannot access them. Marty needs to add users or open the ACLs.

## Participants

The following users are on `sdp173`:

agoetz, mahidhar, mhnguyen, mkandes, mthomas, nickel, ofgarzon, p4rodrig, sfiligoi, sudasgupta, ychen64, zliang7, zonca

## QOS

`sdp173` has the following QOS associations:
- debug-normal
- gpu-debug-normal
- gpu-normal
- gpu-preempt-normal
- gpu-shared-normal
- gpu-shared-eot
- normal
- normal-eot

## Scripts

See `srun-shared.sh`, `srun-compute.sh`, and `srun-gpu.sh` in the repo root for interactive session scripts.

## Testing (July 8, 2026)

- **Shared:** queues (busy)
- **Compute:** works
- **GPU-shared:** queues (busy)

Reservations removed from scripts (restricted to mkandes). Scripts work without reservations.