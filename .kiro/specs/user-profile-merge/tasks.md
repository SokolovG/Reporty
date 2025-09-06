# Implementation Plan

- [x] 1. Create database migration for User-UserProfile merge
  - Create Alembic migration script that adds UserProfile fields to users table
  - Implement data migration logic to copy data from user_profiles to users
  - Update foreign key constraints in task_types table from user_profile_id to user_id
  - Drop user_profiles table after successful data migration
  - _Requirements: 2.2, 2.3, 5.1, 5.2, 5.3, 5.4, 5.5_

- [x] 2. Update User model in SQLAlchemy
  - Add UserProfile fields (display_name, department, position, ai_auto_process, ai_provider_id) to User model
  - Add relationship to AIProvider in User model
  - Add relationship to TaskType in User model
  - Remove UserProfile model class completely
  - _Requirements: 1.1, 1.2, 1.3, 2.1_

- [x] 3. Update TaskType model for direct User relationship
  - Replace user_profile_id field with user_id in TaskType model
  - Update relationship to point directly to User instead of UserProfile
  - Update unique constraint to use user_id instead of user_profile_id
  - Update indexes to use user_id instead of user_profile_id
  - _Requirements: 3.1, 3.2, 3.3_

- [x] 4. Refactor UserRepository for extended User model
  - Update create_user method to handle new profile fields
  - Add methods for updating profile-related fields
  - Remove any UserProfile-related methods if they exist
  - Update all queries to work with the extended User model
  - _Requirements: 4.1, 4.2_

- [x] 5. Update UserService with profile functionality
  - Integrate profile management methods into UserService
  - Update post_registration_hook to handle AI provider setup
  - Add methods for updating user profile information
  - Remove dependencies on ProfileService
  - _Requirements: 4.1, 4.2, 4.3_

- [x] 6. Remove ProfileService and update dependencies
  - Delete ProfileService class
  - Update all imports that reference ProfileService
  - Move any remaining functionality to UserService
  - Update dependency injection configurations
  - _Requirements: 4.1, 4.2_

- [x] 7. Update API controllers for unified User model
  - Merge ProfileController functionality into existing user endpoints
  - Update all profile-related endpoints to work with User model
  - Remove ProfileController class
  - Update DTO classes to work with unified User model
  - _Requirements: 4.3, 4.4_

- [x] 8. Update all service dependencies to use user_id
  - Update TaskService to work with user_id instead of user_profile_id
  - Update any other services that reference UserProfile
  - Ensure all business logic uses user_id consistently
  - _Requirements: 4.2, 4.4_

- [x] 9. Create comprehensive tests for merged User model
  - Write unit tests for updated User model with profile fields
  - Write tests for UserRepository with new functionality
  - Write tests for UserService with integrated profile methods
  - Write integration tests for API endpoints with unified model
  - _Requirements: 4.4_

- [ ] 10. Test and validate migration process
  - Create test database with sample User and UserProfile data
  - Run migration and verify data integrity
  - Test rollback functionality
  - Validate all foreign key relationships work correctly
  - _Requirements: 5.1, 5.2, 5.3, 5.4, 5.5_
