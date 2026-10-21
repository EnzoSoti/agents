---
name: fct-app-v4
description: Complete architecture, module specification, authentication, real-time state conventions, and production deployment guidelines for FCT App V4 (Power Apps Code App + React 19 + TypeScript + Vite).
---

# FCT App V4 - AI Technical Skill & System Map
*Last synchronized on 2026-10-19 16:50:00 based on repository file tree.*

## 1. Executive Summary & Stack
- **Framework**: React 19 + Vite 7 + TypeScript 5.9
- **Platform**: Microsoft Power Apps Code Apps (`@microsoft/power-apps` & `@microsoft/power-apps-vite`)
- **UI & Component System**: Tailwind CSS 3.4 + Lucide React + GSDC Brand Design Tokens
- **State & Real-Time Sync**: Multi-tab `BroadcastChannel` + TanStack Query + `realTimeSyncService` + `loadingManager`
- **Authentication**: JWT / Session Token + Role-Based Access Control (`useAuth` + `ProtectedRoute` + `PermissionGate`)
- **Port Target**: `http://localhost:5174/` (`pac code run --port 1234 --appUrl "http://localhost:5174/"`)
- **Production API Gateway**: `https://fct.203.28.66.38.sslip.io:8443/api` (Caddy reverse proxy + ASP.NET Core 8 Kestrel)
- **Timezone Convention**: Philippine Local Time (PHT / UTC+8). Stored directly in SQL Server `[dbo].[fctFinal]` without artificial UTC shifting (BR-017).
- **Visual Design Standard**: Solid, opaque content cards (zero glassmorphism/blur) paired with calibrated high-visibility GSDC Fleet background watermark (`opacity-35 dark:opacity-40`).

## 2. Core Business Modules & Routing
| Module | Route | Access Level | Primary Source | Functional Scope |
|---|---|---|---|---|
| **Login / Auth** | `/login` | Public | `src/pages/login/LoginPage.tsx` | User authentication, role assignment, and session initialization. |
| **Executive Dashboard** | `/` | Authenticated | `src/pages/dashboard/DashboardPage.tsx` | Summary KPI cards, BU pending breakdown table, and status overview. |
| **Fuel Request** | `/fuel-request` | Authenticated | `src/pages/fuel-request/FuelRequestPage.tsx` | Standardized application form (Driver, Head, Trailer, Odometer, Sukat Tank, Add Blue, Multi-destinations 1-5, Attachments). |
| **Approvals & Issuance** | `/approval` | Approver / Fuel Officer / Admin | `src/pages/approval/ApprovalPage.tsx` | Two-stage workflow: Department Head approval/disapproval and Fuel Officer Tank PO/liters issuance queue with optimistic status caching and PO Copy modal. |
| **Liquidation Monitoring** | `/liquidation` | Auditor / Admin | `src/pages/liquidation/LiquidationPage.tsx` | PO number search, loading verification, auditor sign-off, unliquidated tracking, and real-time live header shortcut counters (Fuel Request Monitoring & FR Disapprove). |
| **Disapproved Registry** | `/disapproved` | Authenticated | `src/pages/disapproved/DisapprovedPage.tsx` | Disapproved requests archive with auditor justifications, rejection history, and vehicle details. |
| **Cancelled Archive** | `/cancelled` | Authenticated | `src/pages/cancelled/CancelledPage.tsx` | Cancelled transactions archive with auditor audit notes and one-click restore-to-queue capabilities (BR-003). |
| **Database Master** | `/database` | Authenticated | `src/pages/database/DatabasePage.tsx` | Central master record repository with multi-field search (PO/OE/Fuel Code), 7-field filter bar, column visibility toggling, and streaming CSV export. |
| **Audit Logs & Changelog** | `/audit-logs` | Auditor / Admin | `src/pages/audit-logs/AuditLogsPage.tsx` | Transaction mutation history, specific reasons, before/after values, and user accountability audit trail (BR-015). |
| **Master Data CRUD** | `/master-data` | Admin / Master Data | `src/pages/master-data/MasterDataPage.tsx` | Fleet tractor heads, trailers, and driver management with full Create/Read/Update/Delete operations (BR-016). |

## 3. Role-Based Access Control (RBAC) Hierarchy
1. **Admin / System Manager**: Full access across all modules, system configuration, master database, audit tools, and cancellation restore.
2. **Approver / Department Head**: Access to Fuel Request, Approvals tab for approving/rejecting requests, and Dashboard.
3. **Fuel Officer**: Access to Issuance queue to assign PO numbers, enter loaded fuel liters, and manage fuel supplies.
4. **Auditor**: Access to Liquidation monitoring, receipt verification, Disapproved archive, Cancelled archive, and Master Database.
5. **Driver / Requester**: Access to filing Fuel Requests, tracking personal request status, and viewing summary logs.

## 4. State & Real-Time Synchronization Protocol
1. **Local & Broadcast Propagation**: Any mutating action (`addTransaction`, `approveRequest`, `issueFuel`, `liquidateTransaction`, `restoreTransaction`) immediately notifies local subscribers and broadcasts a `RealTimeSyncEvent` via `BroadcastChannel` across all open tabs.
2. **Harmonized Caching & TanStack Query**: Secondary tabs listen for broadcast events and automatically synchronize in-memory caches, invalidating query keys (`["dashboard-metrics"]`, `["approval-pending"]`, `["liquidation-list"]`, `["disapproved-list"]`, `["cancelled-list"]`) without requiring a page refresh.
3. **Global Network & Query Progress Bar**: Integrated `loadingManager` (`src/services/loadingManager.ts`) tracks active API fetches and displays a top loading bar (`TopLoadingBar.tsx`), ensuring clear visual feedback on network activity.
4. **User Table Preferences**: `useTablePreferences` hook manages table column visibility, row density (`compact`, `normal`, `comfortable`), and page sizing in local storage per table ID.
5. **Master Data Service**: `src/services/masterDataService.ts` and `src/services/api/masterDataApi.ts` serve as the single source for fetching and caching fleet vehicles, drivers, and operational centers.

## 5. Specialized Feature Modules & UI Primitives
1. **OmniSearch Command Center (`OmniSearchModal.tsx`)**: Global keyboard shortcut (`Ctrl+K` / `Cmd+K`) allowing instant search across Head#, PO#, OE Reference, and Driver names from any screen.
2. **PO Copy Modal (`POCopyModal.tsx`)**: Rapid clipboard export modal formatting issued PO numbers, driver, tractor head, and station info for seamless gas station communication.
3. **Dynamic Real-Time Header Counters**: Reactive badge counters on `LiquidationPage.tsx` providing live visibility into pending approval requests and flagged disapproved queues.
4. **Activity Notification Drawer (`ActivityNotificationDrawer.tsx`)**: Slide-out panel providing a real-time stream of recent changes, approvals, and system notifications.
5. **Origin Badges (`OriginBadge.tsx`)**: Visual badge distinguishing records sourced from SharePoint Online (`SP`), SQL Server Direct (`SQL`), or Manual creation (`MANUAL`).
6. **V3 Table Elements (`V3TableElements.tsx`)**: Specialized UI elements including `POBadgeWithLiters`, `ElapsedHoursBadge`, and status indicators matching FCT App V3 legacy visual requirements.

## 6. Global Alert & Notification System
- **Provider**: `src/components/ui/AlertProvider.tsx` wraps the root layout.
- **Hook**: `useAlert()` provides unified methods for toasts (`success`, `error`, `info`, `warning`) and modal confirmation dialogs.
- **Service**: `src/utils/alertService.ts` provides programmatic triggers accessible outside React component lifecycles.

## 7. Single Source of Truth Configuration & Environments
All environment mappings, connection IDs, and database table targets are centralized in `src/truth.config.ts`, `.env`, and `.env.production`:

### Environment Profiles
| Parameter | Development (`.env`) | Production (`.env.production`) |
|---|---|---|
| `VITE_API_BASE_URL` | `https://fct.203.28.66.38.sslip.io:8443/api` | `https://fct.203.28.66.38.sslip.io:8443/api` |
| `VITE_SHAREPOINT_LIST_TARGET` | `fct2testing` | `fct2testing` |
| `VITE_PORT` | `5174` | `5174` |

### URL Normalization & Deduplication (Poka-Yoke)
All API callers (`apiClient.ts`, `attachmentService.ts`, `headService.ts`, `VersionBanner.tsx`) enforce path deduplication:
- If `VITE_API_BASE_URL` ends in `/api` and an endpoint path begins with `/api/`, the leading `/api` segment is stripped automatically.
- This guarantees requests resolve cleanly as `https://domain.com:8443/api/<route>` instead of invalid double-path `https://domain.com:8443/api/api/<route>`.

### Database & Gateway Targets
- **SQL Gateway Connection**: `aa7b4e76c3b448aaa2a0ea48162d590b` / `b9c5373f724b4d55afa587baaf5b31bf`
- **Database Targets**: `localhost,FCT_Reporting` & `DISPATCH_APP_DMS`
- **SharePoint Attachment Site**: `https://gsdcph.sharepoint.com/sites/ProjectsDevelopments`

## 8. Complete Registered File Inventory
### Page Views (10 files)
- `src/pages/approval/ApprovalPage.tsx`
- `src/pages/audit-logs/AuditLogsPage.tsx`
- `src/pages/cancelled/CancelledPage.tsx`
- `src/pages/dashboard/DashboardPage.tsx`
- `src/pages/database/DatabasePage.tsx`
- `src/pages/disapproved/DisapprovedPage.tsx`
- `src/pages/fuel-request/FuelRequestPage.tsx`
- `src/pages/liquidation/LiquidationPage.tsx`
- `src/pages/login/LoginPage.tsx`
- `src/pages/master-data/MasterDataPage.tsx`

### UI & Layout Components (56 files)
- `src/components/attachments/AttachmentGallery.tsx`
- `src/components/attachments/AttachmentUploader.tsx`
- `src/components/attachments/TransactionAttachmentsGallery.tsx`
- `src/components/audit/AuditDetailModal.tsx`
- `src/components/auth/PermissionGate.tsx`
- `src/components/common/MobileFleetCard.tsx`
- `src/components/common/OriginBadge.tsx`
- `src/components/common/TableToolbar.tsx`
- `src/components/dashboard/FleetAnalyticsOverview.tsx`
- `src/components/database/AdminEditModal.tsx`
- `src/components/filters/BusinessUnitSelector.tsx`
- `src/components/layout/ActivityNotificationDrawer.tsx`
- `src/components/layout/AppShell.tsx`
- `src/components/layout/ErrorBoundary.tsx`
- `src/components/layout/ProtectedRoute.tsx`
- `src/components/layout/Sidebar.tsx`
- `src/components/layout/SplashScreen.tsx`
- `src/components/layout/SyncIndicator.tsx`
- `src/components/layout/Topbar.tsx`
- `src/components/liquidation/CoordinatorLiquidationModal.tsx`
- `src/components/shared/HelpGuideModal.tsx`
- `src/components/shared/ImageAuditViewer.tsx`
- `src/components/shared/OmniSearchModal.tsx`
- `src/components/shared/POCopyModal.tsx`
- `src/components/shared/RemarksPreview.tsx`
- `src/components/shared/RemarksViewerModal.tsx`
- `src/components/shared/TransactionDetailModal.tsx`
- `src/components/ui/Alert.tsx`
- `src/components/ui/AlertDialog.tsx`
- `src/components/ui/AlertProvider.tsx`
- `src/components/ui/Badge.tsx`
- `src/components/ui/Button.tsx`
- `src/components/ui/Card.tsx`
- `src/components/ui/DateRangePresetBar.tsx`
- `src/components/ui/dialog.tsx`
- `src/components/ui/FormSection.tsx`
- `src/components/ui/FullScreenLoadingOverlay.tsx`
- `src/components/ui/Input.tsx`
- `src/components/ui/MetricCard.tsx`
- `src/components/ui/Modal.tsx`
- `src/components/ui/ModalSectionNav.tsx`
- `src/components/ui/OriginBadge.tsx`
- `src/components/ui/PageContainer.tsx`
- `src/components/ui/Pagination.tsx`
- `src/components/ui/RecentUpdateBadge.tsx`
- `src/components/ui/ReturnWorkflowBadge.tsx`
- `src/components/ui/Select.tsx`
- `src/components/ui/Skeleton.tsx`
- `src/components/ui/StatCard.tsx`
- `src/components/ui/Table.tsx`
- `src/components/ui/Tabs.tsx`
- `src/components/ui/Textarea.tsx`
- `src/components/ui/Toast.tsx`
- `src/components/ui/TopLoadingBar.tsx`
- `src/components/ui/V3TableElements.tsx`
- `src/components/ui/VersionBanner.tsx`

### State & Lifecycle Hooks (15 files)
- `src/hooks/AuthContext.tsx`
- `src/hooks/ThemeContext.tsx`
- `src/hooks/useAppInitialization.ts`
- `src/hooks/useApproveTransaction.ts`
- `src/hooks/useAttachments.ts`
- `src/hooks/useAuth.ts`
- `src/hooks/useGlobalKeyboardShortcuts.ts`
- `src/hooks/useMasterData.ts`
- `src/hooks/useModalKeyboard.ts`
- `src/hooks/usePaginatedData.ts`
- `src/hooks/useRealTimeDeltaSync.ts`
- `src/hooks/useRealTimeSync.ts`
- `src/hooks/useTablePreferences.ts`
- `src/hooks/useTheme.ts`
- `src/hooks/useTransactions.ts`

### Data Services & API Layer (17 files)
- `src/services/api/apiClient.ts`
- `src/services/api/auditApi.ts`
- `src/services/api/authApi.ts`
- `src/services/api/dmsApi.ts`
- `src/services/api/masterDataApi.ts`
- `src/services/api/transactionApi.ts`
- `src/services/apiClient.ts`
- `src/services/attachmentService.ts`
- `src/services/authService.ts`
- `src/services/headService.ts`
- `src/services/loadingManager.ts`
- `src/services/masterDataService.ts`
- `src/services/realTimeSync.ts`
- `src/services/sharepoint/fetchSharepointAttachments.ts`
- `src/services/sharepoint/index.ts`
- `src/services/sharepoint/sharePointApi.ts`
- `src/services/sharepoint/sharePointTransactionAdapter.ts`

### TypeScript Data Contracts (5 files)
- `src/types/api.ts`
- `src/types/attachments.types.ts`
- `src/types/audit.ts`
- `src/types/auth.ts`
- `src/types/index.ts`

### Utilities & Helpers (10 files)
- `src/lib/utils.ts`
- `src/utils/alertService.ts`
- `src/utils/attachmentWhitelist.ts`
- `src/utils/cn.ts`
- `src/utils/formatters.ts`
- `src/utils/imageCompression.ts`
- `src/utils/paginatedQueryCache.ts`
- `src/utils/poFormatters.ts`
- `src/utils/transactionQueues.ts`
- `src/utils/workflowHelpers.ts`

## 9. Backend Requests Registry (BR-001 to BR-017)
All backend change requests are organized with dedicated specification files under `backend-requests/`:
- **BR-001**: Connect Frontend to ASP.NET Core 8 Web API
- **BR-002**: Requested and Actual Route Multi-Destination Mapping
- **BR-003**: Cancelled Transactions and Restore Pipeline
- **BR-004**: Master Data Caching and Performance
- **BR-005**: Tractor Head Availability and Changelog Reset
- **BR-006**: SharePoint Attachment Streaming and Special Character Heads
- **BR-007**: Attachment Persistence & Local File Storage Investigation
- **BR-008**: Liquidation Attachment SQL ID Collision & Receipt Sync
- **BR-009**: Queue Filtering, Fuel Code Search & Auditor Sign-off
- **BR-010**: Cancelled Module Status Mapping & KPI Metrics Parity
- **BR-011**: Disapproved & Liquidation Operational Queue Parity
- **BR-012**: Video Attachments & Streaming Support in SharePoint
- **BR-013**: FCT Disapproved Metric & Queue Specification
- **BR-014**: Global Role-Based Access Control (RBAC) & Security Audit
- **BR-015**: Changelog Audit Trail & Specific Reason Logging
- **BR-016**: Master Data Management CRUD API
- **BR-017**: Database Timezone Alignment (Philippine Time PHT / UTC+8)
- **BR-018**: Resolve Production SQL Server Connection Failure & Enable EF Core Transient Error Resiliency

## 10. Mandatory Document & Markdown Landing Policy

Every AI agent working in this project is explicitly instructed to **consult the directory taxonomy map first** whenever creating, generating, or updating any `.md` or `.docx`/`.doc` file.

### Mandatory Landing Lookup Table

| Target File Type | Mandatory Landing Directory |
|---|---|
| **End-User Manuals & SOP Guides (.docx)** | `docs/01-user-manuals/` |
| **UAT Test Matrices & Acceptance Sign-Offs (.docx, .md)** | `docs/02-testing-and-uat/` |
| **System & Module Architecture Specs (.docx)** | `docs/03-system-specifications/` |
| **Workflow & Return/Disapproval Guides (.md)** | `docs/04-workflow-and-feature-guides/` |
| **SharePoint & External Integration Contracts (.md)** | `docs/05-integration-and-api-specs/` |
| **Developer Handbooks, Tokens & Screenshot Guides (.md)** | `docs/06-developer-guides/` |
| **Release Notes & Sprint Deployment Logs (.md)** | `docs/07-sprints-and-releases/` |
| **Formal Backend Change Requests (BR-xxx-*.md)** | `backend-requests/` |
| **Design System Specs & Component Catalogs (.md)** | `design-system/fct-app-v4/` |
| **Dev Server, Proxy & Middleware Scripts** | `scripts/01-dev-server/` |
| **Automated Test Runners & E2E Validation Scripts** | `scripts/02-testing/` |
| **Doc Builders & Word Generator Scripts** | `scripts/03-doc-generators/` |
| **Screenshot Capture & Annotation Automation Scripts** | `scripts/04-screenshot-automation/` |

### Non-Negotiable Rules Enforced on Agents:
1. **Never Save Loose Files in Project Root**: Only `AGENTS.md` is permitted in root. No loose `.md` or `.docx` files.
2. **Never Save Loose Files in `docs/` Root**: Only `docs/README.md` is permitted directly under `docs/`.
3. **Mandatory Indexing**: Any newly created or renamed document must immediately be indexed and linked in `docs/README.md` or `scripts/README.md`.
