package com.security.apisecurity.repository;

import com.security.apisecurity.entity.SsoUser;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.stereotype.Repository;

import java.util.Optional;

@Repository
public interface SsoUserRepository extends JpaRepository<SsoUser, Long> {

    Optional<SsoUser> findByUserId(String userId);

    Optional<SsoUser> findByAccount(String account);
}
