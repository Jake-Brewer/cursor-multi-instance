# Create Multi-Instance Cursor IDE System Project in Linear
param(
    [Parameter(Mandatory=$true)]
    [string]$ApiKey,
    [string]$ProjectName = "Multi-Instance Cursor IDE System",
    [string]$ProjectDescription = "A comprehensive management system for running multiple isolated Cursor IDE instances with custom configurations, AI models, and visual themes. Supports 1-10 simultaneous applications with complete isolation and resource monitoring."
)

Write-Host "Creating Multi-Instance Cursor IDE System project in Linear..." -ForegroundColor Cyan

if (-not $ApiKey.StartsWith("lin_api_")) {
    Write-Host "Invalid API key format. Should start with 'lin_api_'" -ForegroundColor Red
    exit 1
}

try {
    $headers = @{
        "Authorization" = $ApiKey
        "Content-Type" = "application/json"
    }
    
    # First, get the team ID (required for project creation)
    Write-Host "Getting team information..." -ForegroundColor Yellow
    $teamQuery = @{
        query = "{ teams { nodes { id name } } }"
    } | ConvertTo-Json
    
    $teamResponse = Invoke-RestMethod -Uri "https://api.linear.app/graphql" -Method POST -Headers $headers -Body $teamQuery
    
    if ($teamResponse.data.teams.nodes.Count -eq 0) {
        Write-Host "No teams found in your Linear workspace" -ForegroundColor Red
        exit 1
    }
    
    $teamId = $teamResponse.data.teams.nodes[0].id
    $teamName = $teamResponse.data.teams.nodes[0].name
    Write-Host "Using team: $teamName" -ForegroundColor Green
    
    # Create the project
    Write-Host "Creating project: $ProjectName" -ForegroundColor Yellow
    $createProjectQuery = @{
        query = "mutation { projectCreate(input: { name: `"$ProjectName`", description: `"$ProjectDescription`", teamIds: [`"$teamId`"] }) { success project { id name } } }"
    } | ConvertTo-Json
    
    $projectResponse = Invoke-RestMethod -Uri "https://api.linear.app/graphql" -Method POST -Headers $headers -Body $createProjectQuery
    
    if ($projectResponse.data.projectCreate.success) {
        $projectId = $projectResponse.data.projectCreate.project.id
        Write-Host "Project created successfully!" -ForegroundColor Green
        Write-Host "   Project ID: $projectId" -ForegroundColor Gray
        Write-Host "   Project Name: $($projectResponse.data.projectCreate.project.name)" -ForegroundColor Gray
        
        # Create initial development phases and tasks
        Write-Host "`nCreating development phases and tasks..." -ForegroundColor Yellow
        
        $issues = @(
            # Phase 1: System Architecture & Design
            @{
                title = "Design System Architecture"
                description = "Create detailed system architecture for multi-instance management including process isolation, resource allocation, and communication protocols. Requirements: REQ-001 through REQ-008 (Instance Isolation & Concurrent Operations)."
                priority = 1
                labels = @("architecture", "high-priority")
            },
            @{
                title = "Design Launch Interface UI/UX"
                description = "Design the menu/link-based selection interface for launching instances. Must support workspace templates, quick launch options, and visual identification. Requirements: REQ-009 through REQ-012."
                priority = 1
                labels = @("ui-design", "high-priority")
            },
            @{
                title = "Design Resource Monitoring Dashboard"
                description = "Create mockups and specifications for real-time graphical dashboard showing CPU, memory, disk I/O, and network usage per instance. Requirements: REQ-017 through REQ-024."
                priority = 1
                labels = @("ui-design", "monitoring")
            },
            
            # Phase 2: Core Backend Development
            @{
                title = "Implement Instance Management System"
                description = "Build the core system for managing multiple Cursor instances with complete isolation. Must handle process spawning, monitoring, and cleanup. Requirements: REQ-001 through REQ-008."
                priority = 2
                labels = @("backend", "core")
            },
            @{
                title = "Implement Configuration Management"
                description = "Build system for managing workspace configurations with Git versioning. Must support create, edit, delete, clone operations. Requirements: REQ-013 through REQ-016, REQ-039 through REQ-047."
                priority = 2
                labels = @("backend", "configuration")
            },
            @{
                title = "Implement AI Model Configuration System"
                description = "Build per-instance AI model selection and API key management. Support multiple providers (OpenAI, Anthropic). Requirements: REQ-025 through REQ-029."
                priority = 2
                labels = @("backend", "ai-integration")
            },
            
            # Phase 3: Visual & Theme System
            @{
                title = "Implement Color Scheme System"
                description = "Build unique color scheme system per instance for visual identification. Apply to editor themes, UI chrome, window borders, status bars. Requirements: REQ-030 through REQ-033."
                priority = 2
                labels = @("theming", "visual")
            },
            @{
                title = "Create Color Theme Templates"
                description = "Design and implement preset color scheme templates for different use cases (research=blue, customer=green, frontend=purple, backend=red, management=orange). Requirements: REQ-032."
                priority = 3
                labels = @("theming", "templates")
            },
            
            # Phase 4: Resource Monitoring
            @{
                title = "Implement Real-Time Resource Monitor"
                description = "Build system to monitor CPU, memory, disk I/O, network usage per instance with historical tracking. Requirements: REQ-017 through REQ-024, REQ-064 through REQ-070."
                priority = 2
                labels = @("monitoring", "performance")
            },
            @{
                title = "Implement Performance Alerts System"
                description = "Create alert system for resource usage thresholds and instance health monitoring. Requirements: REQ-023, REQ-024."
                priority = 3
                labels = @("monitoring", "alerts")
            },
            
            # Phase 5: Frontend Development
            @{
                title = "Build Launch Interface Frontend"
                description = "Create the main UI for selecting and launching workspace configurations. Must be intuitive and support one-click launching. Requirements: REQ-009 through REQ-012."
                priority = 2
                labels = @("frontend", "core")
            },
            @{
                title = "Build Configuration Management UI"
                description = "Create graphical interface for managing workspace configurations with template system and import/export. Requirements: REQ-013 through REQ-016."
                priority = 2
                labels = @("frontend", "configuration")
            },
            @{
                title = "Build Resource Dashboard Frontend"
                description = "Create real-time dashboard showing resource usage across instances with graphs and health indicators. Requirements: REQ-017 through REQ-024."
                priority = 2
                labels = @("frontend", "monitoring")
            },
            
            # Phase 6: Integration & Testing
            @{
                title = "Implement Environment Variable Management"
                description = "Build per-instance environment variable system for API endpoints, tokens, development settings. Requirements: REQ-056 through REQ-059."
                priority = 3
                labels = @("integration", "environment")
            },
            @{
                title = "Implement System Integration"
                description = "Add Windows shell integration, command-line launching, system tray integration, notifications. Requirements: REQ-060 through REQ-063."
                priority = 3
                labels = @("integration", "system")
            },
            @{
                title = "Create Integration Tests"
                description = "Build comprehensive test suite for all system components including instance isolation, configuration management, and resource monitoring."
                priority = 3
                labels = @("testing", "integration")
            },
            
            # Phase 7: Performance & Polish
            @{
                title = "Performance Optimization"
                description = "Optimize system for 10 concurrent instances with intelligent resource allocation and CPU throttling. Requirements: REQ-064 through REQ-070."
                priority = 3
                labels = @("performance", "optimization")
            },
            @{
                title = "User Experience Polish"
                description = "Refine UI/UX based on testing feedback, ensure visual instance identification within 2 seconds, optimize launch times to under 10 seconds."
                priority = 3
                labels = @("ux", "polish")
            },
            
            # Phase 8: Documentation & Release
            @{
                title = "Create User Documentation"
                description = "Write comprehensive user guides, installation instructions, configuration tutorials, and troubleshooting guides."
                priority = 3
                labels = @("documentation", "user-guides")
            },
            @{
                title = "Beta Testing Program"
                description = "Conduct beta testing with power users managing multiple development projects simultaneously. Gather feedback and iterate."
                priority = 3
                labels = @("testing", "beta")
            },
            @{
                title = "Production Release"
                description = "Final testing, release preparation, and deployment of v1.0 of the Multi-Instance Cursor IDE System."
                priority = 3
                labels = @("release", "production")
            }
        )
        
        $issueCount = 1
        foreach ($issue in $issues) {
            $issueQuery = @{
                query = "mutation { issueCreate(input: { title: `"$($issue.title)`", description: `"$($issue.description)`", teamId: `"$teamId`", projectId: `"$projectId`", priority: $($issue.priority) }) { success issue { id title } } }"
            } | ConvertTo-Json
            
            $issueResponse = Invoke-RestMethod -Uri "https://api.linear.app/graphql" -Method POST -Headers $headers -Body $issueQuery
            
            if ($issueResponse.data.issueCreate.success) {
                Write-Host "   ($issueCount/$($issues.Count)) Created: $($issue.title)" -ForegroundColor Green
            } else {
                Write-Host "   ($issueCount/$($issues.Count)) Failed to create: $($issue.title)" -ForegroundColor Red
                if ($issueResponse.errors) {
                    Write-Host "      Error: $($issueResponse.errors)" -ForegroundColor Red
                }
            }
            $issueCount++
            Start-Sleep -Milliseconds 500  # Rate limiting
        }
        
        Write-Host "`nMulti-Instance Cursor IDE System project setup completed!" -ForegroundColor Green
        Write-Host "Created $($issues.Count) development tasks across 8 phases" -ForegroundColor Blue
        Write-Host "Phase 1: System Architecture & Design (2 tasks)" -ForegroundColor Gray
        Write-Host "Phase 2: Core Backend Development (3 tasks)" -ForegroundColor Gray
        Write-Host "Phase 3: Visual & Theme System (2 tasks)" -ForegroundColor Gray
        Write-Host "Phase 4: Resource Monitoring (2 tasks)" -ForegroundColor Gray
        Write-Host "Phase 5: Frontend Development (3 tasks)" -ForegroundColor Gray
        Write-Host "Phase 6: Integration & Testing (3 tasks)" -ForegroundColor Gray
        Write-Host "Phase 7: Performance & Polish (2 tasks)" -ForegroundColor Gray
        Write-Host "Phase 8: Documentation & Release (3 tasks)" -ForegroundColor Gray
        Write-Host "`nYou can now view the project and all tasks in your Linear workspace" -ForegroundColor Blue
        Write-Host "GitHub Repository: https://github.com/Jake-Brewer/cursor-multi-instance" -ForegroundColor Blue
        
    } else {
        Write-Host "Failed to create project" -ForegroundColor Red
        if ($projectResponse.errors) {
            Write-Host "Errors: $($projectResponse.errors)" -ForegroundColor Red
        }
    }
    
} catch {
    Write-Host "Error: $($_.Exception.Message)" -ForegroundColor Red
    if ($_.Exception.Message -like "*401*") {
        Write-Host "Check your API key permissions" -ForegroundColor Yellow
    }
} 