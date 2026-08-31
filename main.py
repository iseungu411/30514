// [3D 보스 - 화염 마룡 드래곤 (Red Dragon)]
        const boss = new THREE.Group();
        
        // 1. 드래곤 몸통 (거대한 붉은 메쉬)
        const bBodyMat = new THREE.MeshStandardMaterial({ color: 0x990000, roughness: 0.3, metalness: 0.8 });
        const bBody = new THREE.Mesh(new THREE.DodecahedronGeometry(1.4, 1), bBodyMat);
        boss.add(bBody);

        // 2. 드래곤 머리 & 입
        const headMat = new THREE.MeshStandardMaterial({ color: 0xcc0000, metalness: 0.9 });
        const head = new THREE.Mesh(new THREE.ConeGeometry(0.7, 1.5, 5), headMat);
        head.position.set(-0.8, 0.8, 0.5);
        head.rotation.z = Math.PI / 3;
        head.rotation.y = -Math.PI / 6;
        boss.add(head);

        // 3. 붉게 빛나는 눈 (Point Light 및 소형 메쉬)
        const eyeMat = new THREE.MeshBasicMaterial({ color: 0xffff00 });
        const eye = new THREE.Mesh(new THREE.SphereGeometry(0.15, 8, 8), eyeMat);
        eye.position.set(-1.1, 1.1, 0.8);
        boss.add(eye);

        // 4. 거대한 화염 날개 (양쪽 2개)
        const wingMat = new THREE.MeshBasicMaterial({ color: 0xff3300, wireframe: true });
        const wingLeft = new THREE.Mesh(new THREE.PlaneGeometry(2.5, 2.5), wingMat);
        wingLeft.position.set(1.2, 1.2, -1);
        wingLeft.rotation.y = Math.PI / 4;
        
        const wingRight = new THREE.Mesh(new THREE.PlaneGeometry(2.5, 2.5), wingMat);
        wingRight.position.set(1.2, 1.2, 1);
        wingRight.rotation.y = -Math.PI / 4;
        
        boss.add(wingLeft);
        boss.add(wingRight);

        // 5. 화염 회전 아우라
        const bAura = new THREE.Mesh(
            new THREE.TorusGeometry(2.2, 0.08, 16, 100),
            new THREE.MeshBasicMaterial({ color: 0xff6600, wireframe: true })
        );
        bAura.rotation.x = Math.PI / 2;
        boss.add(bAura);

        boss.position.set(3, 1.0, 0);
        scene.add(boss);
